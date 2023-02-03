import requests
import datetime as dt
import os

from sqlalchemy.orm import Session
from dotenv import load_dotenv

from . import models, schemas


load_dotenv(dotenv_path='.env')
APPID = os.getenv('APPID')

# Вспомогательные функции
# 1. Подсчет количества городов в БД
def count_cities(db: Session) -> int:
    return db.query(models.City).count()


# 2. Получение city.id по названию города (city.name)
def get_city_id(db: Session, city_name: str) -> int:
    """Returns id (int) of the given city name (str)."""
    return db.query(models.City).filter(models.City.name == city_name).first().id


# 3. Подсчет среднего значения заданного параметра (column_name) для определенного города
def count_avg(db: Session, city_id: int, column_name: str):
    """Returns key-value (dict). Key - avg_<column_name>. Value - average value of the given parameter (column)."""
    query = db.execute(
        f"""
        SELECT AVG({column_name}) as avg_{column_name}
        FROM weather_info 
        WHERE city_id = {city_id}
        """
        ).first()
    return query
    

# 5. Функция поиска города на openweather. Возвращает координаты города в виде словаря
def city_coordinates(city_name: str):
    """If the city is in openweather.com then returns its' coordinates {'lan': .., 'lat': ..}, otherwise returns None"""
    url = 'http://api.openweathermap.org/geo/1.0/direct?'
    params = {
        'q': city_name,
        'appid': APPID,
    }
    response = requests.get(url=url, params=params).json()
    if city_name.title() in response[0]['name']:
        return {
            'lat': response[0]['lat'],
            'lon': response[0]['lon']
        }


def city_list(db: Session):
    """Returns a list of all cities in database"""
    return db.query(models.City).all()
    

# Проверка наличия города в базе данных
def city_in_db(db: Session, city_name: str) -> bool:
    """Checks if city is already in the database"""
    db_city_check = db.query(models.City).filter_by(name=city_name).first()
    if db_city_check == None:
        return False
    return True


# Целевые функции
# 1. Возвращает список существующих городов с последней записанной температурой
def get_last_weather(db: Session, search: str | None):
    query = []
    if search != None:
        query.append(db.execute(
            f"""
            SELECT * 
            FROM weather_info 
            WHERE city_name LIKE '%{search.capitalize()}%'
            ORDER BY date_time DESC  
            """).first())

    else:   
        city_ids = [x['id'] for x in db.query(models.City.id).all()]
        for id in city_ids:
            query.append(db.execute(
                f"""
                SELECT * 
                FROM weather_info 
                WHERE city_id = {id}
                ORDER BY date_time DESC  
                """).first())
    return query

# def get_last_weather(db: Session):
#     city_names = [x['name'] for x in db.query(models.City.name).all()]
#     query = []
#     for name in city_names:
#         query.append(db.execute(
#             f"""
#             SELECT * 
#             FROM weather_info 
#             WHERE city_name = {name}
#             ORDER BY date_time DESC  
#             """).first())
#     return query


# 2. По заданному городу возвращает все данные за выбранный период, а также их средние значения за этот период
def get_city_stats(
    db: Session, 
    city: str, 
    date_time_start=dt.datetime(year=2023, month=1, day=1), 
    date_time_end=dt.datetime.now()
    ):
    city_id = get_city_id(db=db, city_name=city.title())

    records = db.query(models.WeatherInfo).filter(
            models.WeatherInfo.city_id == city_id, 
            date_time_start <= models.WeatherInfo.date_time,
            date_time_end >= models.WeatherInfo.date_time
            ).all()
    average_values = {
        **count_avg(db=db, city_id=city_id, column_name='temperature'),
        **count_avg(db=db, city_id=city_id, column_name='atm_pressure'),
        **count_avg(db=db, city_id=city_id, column_name='wind_speed')
        }
    return {'average_valus': average_values, 'records': records, }
    

# 3. Добавляет город в БД, если он есть на openweather
def add_city(db: Session, city: str):
    coord = city_coordinates(city_name=city)
    if coord != None:
        lat = coord['lat']
        lon = coord['lon']
        db_city = models.City(name=city.title(), lat=lat, lon=lon)
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city

