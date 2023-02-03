import scrapy
import json
import os

from datetime import datetime
from dotenv import load_dotenv

from db import models, crud, database


load_dotenv(dotenv_path='../.env')
APPID = os.getenv('APPID')


class WeatherSpider(scrapy.Spider):
    name = "weather"

    def __init__(self):
        # Создаем сессию для работы с базой данных внутри WeatherSpider
        self.db = database.SessionLocal()

    # Функция возвращает список urls, в котором url для каждого города из БД
    def get_urls(self) -> list:
        cities = crud.city_list(self.db)
        urls = []
        for city in cities:
            urls.append(f"https://api.openweathermap.org/data/2.5/weather?lat={city.lat}&lon={city.lon}&units=metric&appid={APPID}")
        return urls

    
    def start_requests(self):
        urls = self.get_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        # Из запроса получаем необходимые данные
        jsonresponse = json.loads(response.body)
        city = jsonresponse['name']
        temperature = jsonresponse['main']['temp']
        atm_pressure = jsonresponse['main']['pressure']
        wind_speed = jsonresponse['wind']['speed']

        # Записываем данные в БД
        db_weather_info = models.WeatherInfo(
            # TODO: get city_name from db with its' coordinates
            city_id=crud.get_city_id(db=self.db, city_name=city),
            city_name=city,
            date_time=datetime.now(),
            temperature=temperature,
            atm_pressure=atm_pressure,
            wind_speed=wind_speed
            )
        self.db.add(db_weather_info)
        self.db.commit()

