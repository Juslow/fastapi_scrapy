from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    lon = Column(Float)
    lat = Column(Float)

    weather_info = relationship("WeatherInfo", back_populates="city")


class WeatherInfo(Base):
    __tablename__ = "weather_info"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    city_name = Column(String(64))
    date_time = Column(DateTime)
    temperature = Column(Float)
    atm_pressure = Column(Float)
    wind_speed = Column(Float)

    city = relationship("City", back_populates="weather_info")