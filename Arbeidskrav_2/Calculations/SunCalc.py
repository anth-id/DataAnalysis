import pandas as pd



class SunCalc:
    '''
    1. Makes a copy of df that is inserted into the class. This is apparently good for data integrity since the changes in the df wont affect the original.
    2. Pick out the date from the df, convert into datetime values. Otherwise we would get AttributeError: Can only use .dt accessor with datetimelike values.
    3. In our database we store day length in seconds. Now we make a convert seconds to hours and make a new column as day_len hours. 
    4. We create a new column named month. For each date in each month it assings a value 1-12 depending on the month. Ex january = 1
    '''
    def __init__(self, df: pd.DataFrame ) -> None:
        self.df: pd.DataFrame = df.copy()
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["daylen_hours"] = self.df["day_length_seconds"] /3600
        self.df["month"] = self.df["date"].dt.month




    '''
    1. This method makes a new DataFrame from the class innit method. It makes a pivot table on self.df and saves as df cleaned.
    2. Every city get its column, each month a row. Then we use aggfunc to get the mean on all day length hours. 
    3. Return the table with one decimal on our day length hours. 
    
    '''

    def avg_daylength_p_month(self) -> pd.DataFrame:
        df_cleaned:pd.DataFrame = self.df.pivot_table(
            index="month",
            columns="city",
            values="daylen_hours",
            aggfunc="mean"
        )
        return df_cleaned.round(1)
     
        