import os
from os import getcwd
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

class ScrapeJob(Base):
    __tablename__ = "scrape_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    status = Column(String, default="pending")
    result = Column(Text)


db_file = os.path.join(getcwd(), "scrape_jobs.db")

os.makedirs(os.path.dirname(db_file), exist_ok=True)

engine = create_engine(f"sqlite:///{db_file}")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

try:
    with Session() as session:
        session.query(ScrapeJob).first()
except Exception as e:
    print("Error connecting to database", e)
