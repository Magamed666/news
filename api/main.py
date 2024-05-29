from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "mysql+pymysql://root:example@db/news_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Source(Base):
    __tablename__ = "source"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(2048), nullable=False)
    config = Column(JSON, nullable=False)

class SourceCreate(BaseModel):
    name: str
    url: str
    config: dict

Base.metadata.create_all(bind=engine)

@app.post("/sources/")
def create_source(source: SourceCreate):
    db = SessionLocal()
    db_source = Source(name=source.name, url=source.url, config=source.config)
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    db.close()
    return db_source

@app.get("/sources/{source_id}")
def read_source(source_id: int):
    db = SessionLocal()
    source = db.query(Source).filter(Source.id == source_id).first()
    db.close()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

@app.put("/sources/{source_id}")
def update_source(source_id: int, source: SourceCreate):
    db = SessionLocal()
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if db_source is None:
        db.close()
        raise HTTPException(status_code=404, detail="Source not found")
    db_source.name = source.name
    db_source.url = source.url
    db_source.config = source.config
    db.commit()
    db.refresh(db_source)
    db.close()
    return db_source

@app.delete("/sources/{source_id}")
def delete_source(source_id: int):
    db = SessionLocal()
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if db_source is None:
        db.close()
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(db_source)
    db.commit()
    db.close()
    return {"detail": "Source deleted"}
