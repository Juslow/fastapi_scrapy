# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CrawlingPipeline:

    # def __init__(self):
    #     self.db = SessionLocal()


    def process_item(self, item, spider):
        self.create_weather_record(item)
        return item

    # def create_weather_record(self, item):
    # db_weather_info = WeatherInfo(
    #     city=item['city'],
    #     date_time=datetime.now(),
    #     temperature=item['temperature'],
    #     atm_pressure=item['atm_pressure'],
    #     wind_speed=item['wind_speed']
    #     )
    # self.db.add(db_weather_info)
    # self.db.commit()