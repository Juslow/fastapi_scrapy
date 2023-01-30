import scrapy
import json
from ..items import TutorialItem


lon = 37.62
lat = 55.75
appid = '12ccdf79474e14750faf353df0a149dc'

class WeatherSpider(scrapy.Spider):
    name = "weather"

    # time = datetime.now()

    # for city in db.Cities ...
    #   lon = db.Cities.lon
    #   lat = db.Cities.lat
    start_urls = [f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={appid}', 
    f'https://api.openweathermap.org/data/2.5/weather?lat=40.71&lon=-74.01&units=metric&appid={appid}']


    def parse(self, response):

        items = TutorialItem()

        jsonresponse = json.loads(response.body)
        city = jsonresponse['name']
        temperature = jsonresponse['main']['temp']
        atm_pressure = jsonresponse['main']['pressure']
        wind_speed = jsonresponse['wind']['speed']

        items['city'] = city
        items['temperature'] = temperature
        items['atm_pressure'] = atm_pressure
        items['wind_speed'] = wind_speed
        # items['time'] = time

        yield items
 