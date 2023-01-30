from pydantic import BaseModel
from datetime import datetime


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    lon: float
    lat: float

    class Config:
        orm_mode = True


class WeatherInfoBase(BaseModel):
    city_id: int
    temperature: float
    atm_pressure: float
    wind_speed: float
    date_time: datetime


class WeatherInfoCreate(WeatherInfoBase):
    pass


class WeatherInfo(WeatherInfoBase):
    id: int

    class Config:
        orm_mode = True