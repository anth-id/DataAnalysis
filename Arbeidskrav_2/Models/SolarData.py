from datetime import datetime
from datetime import timedelta


class SolarData:

    @staticmethod
    def parse_time(value:str | None) -> datetime | None:
        if value is None:
            return None
        return datetime.fromisoformat(value)

    @staticmethod
    def format_time(value:datetime | None) -> str | None:
        if value is None:
            return "N/A"
        return value.strftime("%H:%M:S")



    def __init__(self, rec:dict):
        seconds:int | None = rec['day_length']
        self.date = rec['date']
        self.moon_illumination:float = rec['moon_illumination']
        self.sunrise_azimuth:float = rec['solar_position']['sunrise_azimuth']
        self.solar_noon_altitude:float = rec['solar_position']['solar_noon_altitude']
        self.sunset:datetime | None = self.parse_time(rec['sunset'])
        self.sunrise:datetime | None = self.parse_time(rec['sunrise'])
        self.daylen:timedelta | None = None if seconds is None else timedelta(seconds=rec['day_length'])
        self.daylen_seconds:int | None = seconds
        self.daylen_hours:float | None = None if seconds is None else seconds / 3600
        self.moon_phase:str = rec['moon_phase']

    def __str__(self) -> str:
        return (
            f"Date: {self.date}\n"
            f"Moon illumination: {self.moon_illumination}%\n"
            f"Sunrise azimuth: {self.sunrise_azimuth}\n"
            f"Solar noon altitude: {self.solar_noon_altitude}\n"
            f"Sunset: {self.format_time(self.sunset)}\n"
            f"Sunrise: {self.format_time(self.sunrise)}\n"
            f"Daylength: {self.daylen}\n"
            f"Daylength_seconds: {self.daylen_seconds}\n"
            f"Moonphase: {self.moon_phase}"
        )