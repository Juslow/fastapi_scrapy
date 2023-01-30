from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime


import db.crud as crud, db.database as database, db.models as models, db.schemas as schemas
# from . import crud, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/weather/{city}", response_model=schemas.City)
def weather_city(city: str, db: Session=Depends(get_db)):
    # Проверка наличия города в базе данных
    if crud.city_in_db(db=db, city_name=city):
        raise HTTPException(status_code=404, detail="The city is already in the database")
    city_db = crud.add_city(db=db, city=city)
    # Проверка наличия города на сайте openweather.
    if city_db == None:
        raise HTTPException(status_code=404, detail="City not found")
    return city_db