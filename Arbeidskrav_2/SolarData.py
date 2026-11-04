from datetime import datetime
from datetime import timedelta

class SolarData:
    def __init__(self, rec:dict):
        self.moon_illumination:float = rec['moon_illumination']
        self.sunrise_azimuth:float = rec['solar_position']['sunrise_azimuth']
        self.sunrise_azimuth:float = rec['solar_position']['sunrise_azimuth']
        self.solar_noon_altitude:float = rec['solar_position']['solar_noon_altitude']
        self.sunset:datetime = datetime.fromisoformat(rec['sunset'])
        self.sunrise:datetime = datetime.fromisoformat(rec['sunrise'])
        self.daylen:timedelta = timedelta(rec['day_length'])
        self.daylen_seconds:int = rec['day_length']

    def __str__(self) -> str:
        return (
            f"Moon illumination: {self.moon_illumination}\n"
            f"Sunrise azimuth: {self.sunrise_azimuth}\n"
            f"Solar noon altitude: {self.solar_noon_altitude}\n"
            f"Sunset: {self.sunset.strftime('%H:%M:%S')}\n"
            f"Sunrise: {self.sunrise.strftime('%H:%M:%S')}\n"
            f"Daylength: {self.daylen}\n"
            f"Daylength_seconds: {self.daylen_seconds}"
        )