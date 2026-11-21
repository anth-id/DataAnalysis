from Models.SolarData import SolarData
from Models.GeoData import GeoData
import psycopg2


class SolarDataDb:
    def __init__(self, dburl:str):
        try:
            self.conn = psycopg2.connect(dburl)
        except Exception as e:
            print( "Failed to connect to database.")
            raise e

    def getcity(self, geo:GeoData) -> int:
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('''
                INSERT INTO city (city_name, lat, lon)
                VALUES (%s, %s, %s)
                ON CONFLICT (city_name, lat, lon)
                DO UPDATE SET city_name = EXCLUDED.city_name
                RETURNING id''', (geo.city, geo.lat, geo.lon)
                )
                row = cursor.fetchone()
                if row is None:
                    raise RuntimeError (f"Couldnt get id for {geo.city}")
                else:
                    city_id:int = row[0]
            self.conn.commit()
            return city_id
                
        except Exception:
            self.conn.rollback()
            raise


    def insert(self, city_id:int, solar:SolarData):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute('''
                INSERT INTO solar_day (city_id, date, sunrise, sunset, day_length_seconds, sunrise_azimuth, solar_noon_altitude, moon_illumination)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (city_id, date) DO NOTHING
                ''', (city_id, solar.date, solar.sunrise, solar.sunset,
                solar.daylen_seconds, solar.sunrise_azimuth,
                solar.solar_noon_altitude, solar.moon_illumination)
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise


    def retrieve(self, cities: list[str] ) -> pd.DataFrame:
        "Gives aliases to city(c) and solar_day(s)"
        sql:str = '''
            SELECT c.city_name AS city, s.date, s.sunrise, s.sunset, 
            s.day_length_seconds, s.sunrise_azimuth, s.solar_noon_altitude, s.moon_illumination
            FROM solar_day AS s
            JOIN city AS c on c.id = s.city_id
            '''
            #Continue here 
    

    def close(self) -> None :
        self.conn.close()


                



        
