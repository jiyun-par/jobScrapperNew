from flask import Flask, render_template,request,redirect, send_file
from indeed import get_jobs as indeed_jobs
from wework import get_jobs as wework_jobs
from remoteok import get_jobs as remoteok_jobs
from exporter import save_to_file

db={}

app = Flask("SupperScrapper")
@app.route("/")
def home():
  return render_template("intro.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower().replace(" ","")
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      indeed = indeed_jobs(word)
      wework = wework_jobs(word)
      remoteok = remoteok_jobs(word)
      jobs = indeed + wework + remoteok
      db[word] =jobs
  else:
    redirect("/")
  return render_template(
    "report.html",
    word=word,
    resultsNumber = len(jobs),
    jobs=jobs
  )
    
@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower().replace(" ","")
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs,word)
    return send_file(f"{word}.csv")
  except:
    return redirect("/")
 #hey
    
app.run(host="0.0.0.0")