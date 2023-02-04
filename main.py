import asyncio
import subprocess

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from db import crud, database, models, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def run_spider():
    while True:
        try:
            await asyncio.get_event_loop().run_in_executor(None, run_spider_sync)
        except Exception as e:
            print(f"Error running Scrapy spider: {e}")
        await asyncio.sleep(60)


def run_spider_sync():
    subprocess.run(["scrapy", "runspider", "crawler.py"], 
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE,
            check=True
    )


# С запуском программы запускает scrapy spider
@app.on_event("startup")
async def start_background_tasks():
    loop = asyncio.get_event_loop()
    loop.create_task(run_spider())


@app.post("/weather/{city}", response_model=schemas.City)
async def weather_city(city: str, db: Session=Depends(get_db)):
    # Проверка наличия города в базе данных
    if crud.city_in_db(db=db, city_name=city):
        raise HTTPException(status_code=404, detail="The city is already in the database")
    city_db = crud.add_city(db=db, city=city)
    # Проверка наличия города на сайте openweather.
    if city_db == None:
        raise HTTPException(status_code=404, detail="City not found")
    return city_db


@app.get("/last_weather")
async def last_weather(db: Session=Depends(get_db), search: str=None):
    return crud.get_last_weather(db=db, search=search)


@app.get("/city_stats")
def city_stats(
    db: Session=Depends(get_db), 
    city: str=None, 
    date_time_start: str="2023-01-01-00-00", 
    date_time_end: str="2099-01-01-00-00",
    ):
    
    date_format = "%Y-%m-%d-%H-%M"

    try:
        date_start_dt = datetime.strptime(date_time_start, date_format)
        date_end_dt = datetime.strptime(date_time_end, date_format)

        return crud.get_city_stats(
            db=db, 
            city=city, 
            date_time_start=date_start_dt,
            date_time_end=date_end_dt
            )
    except ValueError:
        raise HTTPException(
            status_code=401, 
            detail="Wrong data format. For date_time use format yyyy-mm-dd-hour-minute (%Y-%m-%d-%H-%M)")

    except AttributeError:
        raise HTTPException(
            status_code=401, 
            detail=f"{city} not in database")
