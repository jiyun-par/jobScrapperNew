import requests
from bs4 import BeautifulSoup



def job_list(word,URL):
  jobs = []
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
  results = requests.get(f"{URL}/remote-{word}-jobs",headers=headers)
  soup = BeautifulSoup(results.text, 'html.parser')
  section = soup.find("div",{"class","page"}).find("div",{"class","container"})
  job_table = section.find("table").find_all("tr",{"class","job"})
  for list in job_table:
    job = extract_job(list,URL)
    jobs.append(job)
  return jobs


def extract_job(list,URL):
  company = list["data-company"]
  get_info =list.find("td",{"class","company"})
  location = get_info.find("div",{"class","location"})
  if location is not None:
    location = location.get_text(strip=True)
  else:
    return;
  title = get_info.find("a",{"class","preventLink"}).find("h2").get_text(strip=True)
  link = list["data-href"]
  return {"title":title,"company":company,"location":location,"link":f"{URL}{link}"}


  
def get_jobs(word):
  URL = f"https://remoteok.com"
  jobs = job_list(word,URL)
  return jobs
