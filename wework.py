import requests
from bs4 import BeautifulSoup



def job_list(word,URL):
  jobs = []
  results = requests.get(f"{URL}/remote-jobs/search?&term={word}")
  soup = BeautifulSoup(results.text, 'html.parser')
  job_section = soup.find("section",{"class","jobs"})
  job_lists = job_section.find_all("li",{"class","feature"})

  for list in job_lists:
    anchor = list.find("div",{"class","tooltip"}).next_sibling
    job = extract_job(anchor,URL)
    jobs.append(job)
  return jobs


def extract_job(anchor,URL):
  company = anchor.find("span",{"class","company"}).get_text(strip=True)
  location = anchor.find("span",{"class","region"}).get_text(strip=True)
  title = anchor.find("span",{"class","title"}).get_text(strip=True)
  link = anchor["href"]
  return {"title":title,"company":company,"location":location,"link":f"{URL}{link}"}


  
def get_jobs(word):
  URL = f"https://weworkremotely.com"
  jobs = job_list(word,URL)
  return jobs
