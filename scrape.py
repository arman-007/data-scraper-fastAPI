import requests
from bs4 import BeautifulSoup
from models import ScrapeJob, Session

def scrape_url(job_id, url: str):
    session = Session()
    job = session.query(ScrapeJob).get(job_id)
    job.status = "in_progress"
    session.commit()

    for attempt in range(3):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else "No title found"
                job.result = f"Title: {title}"
                job.status = "completed"
                break
            else:
                job.status = "failed"
                job.result = f"Failed to retrieve the URL. Status code: {response.status_code}"
        except Exception as e:
            if attempt < 2:
                continue
            else:
                job.result = f"Error: {str(e)}"
        finally:
            session.commit()
            session.close()
                
