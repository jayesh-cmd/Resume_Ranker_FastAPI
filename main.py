from fastapi import FastAPI , UploadFile , File , Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from model import process_resumes


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_homepage():
    return FileResponse("static/index.html")


@app.get("/")
def welcome():
    return {"Welcome" : "Welcome To Resume Ranker API"}

@app.post("/rank")
async def rank_resumes(job_description : str=Form() , files: List[UploadFile] = File()):
    return await process_resumes(job_description , files)