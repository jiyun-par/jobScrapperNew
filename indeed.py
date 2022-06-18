import requests
from bs4 import BeautifulSoup
LIMIT = 100


def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  pagination = soup.find("ul",{"class":"pagination-list"})
  links = pagination.find_all("a")
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_job(html,url):
  title_box = html.find("h2",{"class":"jobTitle"})
  actual_title = title_box.find("a").find("span")["title"]
  company = html.find("span",{"class","companyName"}).string.strip()
  location = html.find("div",{"class","companyLocation"})
  location = str(location.string)
  job_id = html.find("a")["data-jk"]
  return {"title":actual_title,"company":company,"location":location,"link":f"{url}&vjk={job_id}"}

def extract_jobs(last_page,url):
  jobs= []
  for page in range(last_page):
    print(f"Scrapping indeed page {page}")
    result = requests.get(f"{url}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("table",{"class":"jobCard_mainContent"})
    for result in results:
     job = extract_job(result,url)
     jobs.append(job)
  print("success!")
  return jobs

def get_jobs(word):
  url = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page,url)
  return jobs