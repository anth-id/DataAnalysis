import pandas as pd



class SunCalc:
    '''
    1. Makes a copy of df that is inserted into the class. This is apparently good for data integrity since the changes in the df wont affect the original.
    2. Pick out the date from the  from the df, convert into 
    '''
    def __init__(self, df: pd.DataFrame ) -> None:
        self.df: pd.DataFrame = df.copy()
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["daylen_hours"] = self.df["day_length_seconds"] /3600
        self.df["month"] = self.df["date"].dt.month
        print(self.df[["city", "date", "month", "daylen_hours"]].head())
        



    def avg_daylength_p_month(self) -> pd.DataFrame:
        df:pd.DataFrame = self.df.pivot_table(
            index="month",
            columns="city",
            values="daylen_hours",
            aggfunc="mean"
        )
        return df.round(1)
     
        