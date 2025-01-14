from fastapi import FastAPI, HTTPException, Depends, Header
from models import ScrapeJob, Session
from contextlib import asynccontextmanager
import multiprocessing

from scrape import scrape_url


AUTH_TOKEN = "1234567890"
pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    yield

    pool.colse()
    pool.join()


app = FastAPI(lifespan=lifespan)

def verify_token(x_auth_token: str = Header(...)):
    if x_auth_token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    

@app.post("/submit", dependencies=[Depends(verify_token)])
async def submit_scrape_job(url: str):
    session = Session()
    new_job = ScrapeJob(url=url)
    session.add(new_job)
    session.commit()

    #web scraping logic here
    pool.apply_async(scrape_url, args=(new_job.id, new_job.url))

    return {"job_id": new_job.id, "status": "submitted"}

@app.get("/status/{job_id}", dependencies=[Depends(verify_token)])
def get_status(job_id: int):
    session = Session()
    job = session.query(ScrapeJob).get(job_id)

    if not job:
        return {"error" : "Job not found"}
    return {"job_id": job.id, "status": job.status, "result": job.result}
