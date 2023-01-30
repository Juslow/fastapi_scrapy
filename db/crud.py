from sqlalchemy.orm import Session
import requests
import datetime as dt

from . import models, schemas
# import models, schemas

API_KEY = '12ccdf79474e14750faf353df0a149dc'


# Вспомогательные функции
# 1. Подсчет количества городов в БД
def count_cities(db: Session) -> int:
    return db.query(models.City).count()


# 2. Получение city.id по названию города (city.name)
def get_city_id(db: Session, city_name: str) -> int:
    """Returns id (int) of the given city name (str)."""
    return db.query(models.City).filter_by(name=city_name.title()).first().id


# 3. Подсчет среднего значения 
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
    

# 4. Запись информации о погоде для одного города
def create_weather_record(db: Session, weather_info: schemas.WeatherInfo):
    db_weather_info = models.WeatherInfo(**weather_info.dict())
    db.add(db_weather_info)
    db.commit()
    db.refresh(db_weather_info)
    return db_weather_info


# 5. Функция поиска города на openweather. Возвращает координаты города в виде словаря
def city_coordinates(city_name: str):
    """If city is in openweather.com then returns it's coordinates {'lan': .., 'lat': ..}, otherwise returns None"""
    url = 'http://api.openweathermap.org/geo/1.0/direct?'
    params = {
        'q': city_name,
        'appid': API_KEY,
    }
    response = requests.get(url=url, params=params).json()
    if response[0]['name'] == city_name.title():
        return {
            'lat': response[0]['lat'],
            'lon': response[0]['lon']
        }


def city_in_db(db: Session, city_name: str) -> bool:
    """Checks if city is already in the database"""
    db_city_check = db.query(models.City).filter_by(name=city_name).first()
    if db_city_check == None:
        return False
    return True


# Целевые функции
# 1. Возвращает список существующих городов с последней записанной температурой
def get_last_weather(db: Session):
    city_ids = [x['id'] for x in db.query(models.City.id).all()]
    query = []
    for id in city_ids:
        query.append(db.execute(
            f"""
            SELECT * 
            FROM weather_info 
            WHERE city_id = {id}
            ORDER BY date_time DESC  
            """).first())
    return query


# 2. По заданному городу возвращает все данные за выбранный период, а также их средние значения за этот период
def get_city_stats(
    db: Session, 
    city: str, 
    date_time_start=dt.datetime(year=2023, month=1, day=1), 
    date_time_end=dt.datetime.now()
    ):
    city_id = get_city_id(db=db, city_name=city.title())
    return db.query(models.WeatherInfo).filter(
            models.WeatherInfo.city_id == city_id, 
            date_time_start <= models.WeatherInfo.date_time,
            date_time_end >= models.WeatherInfo.date_time
            ).all()
    

# 3. Добавить город в БД, если он есть на openweather
def add_city(db: Session, city: str):
    coord = city_coordinates(city_name=city)
    if coord != None:
        lat = coord['lat']
        lon = coord['lon']
        db_city = models.City(name=city, lat=lat, lon=lon)
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city


# 4. Запись информации о погоде для всех городов в БД в данный момент времени
# def get_weather(db: Session):
#     cities = db.query(models.City).all()
#     for city in cities:
#         create_weather_record(db=db, )