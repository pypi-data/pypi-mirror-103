import os
import numpy as np
import pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects import FloatVector, numpy2ri
from datetime import datetime


base = importr('base')
utils = importr('utils')
pth = os.path.abspath(os.getcwd())

stats = importr('stats')
graphics = importr('graphics')
grdevices = importr('grDevices')


try:
    base.suppressWarnings(utils.install_packages("forecast"))
except:
    pass

try:
    ahead = importr('ahead')
except:
    base.suppressWarnings(utils.install_packages("ahead",
                                                 repos=pth + "/r-ahead-forge",
                                                 type="source"))
    ahead = importr('ahead')


class DynamicRegressor():

    def __init__(self, h=5, level=95, 
                 weights=[1/3, 1/3, 1/3], 
                 pi="E", date_formatting="original"):
        
        self.h = h
        self.level = level
        self.weights = weights
        self.pi = pi
        self.date_formatting=date_formatting

        self.fcast = None
        self.averages = None
        self.ranges = None        


    def forecast(self, df):            
        
        # obtain dates 'forecast' -----

        input_dates = df['date'].values 
        n_input_dates = len(input_dates)        
        input_dates_ms = [datetime.strptime(str(input_dates[i]), "%Y-%m-%d").timestamp()*1000 for i in range(n_input_dates)]    

        frequency = pd.infer_freq(pd.DatetimeIndex(input_dates))
        output_dates = np.delete(pd.date_range(start=input_dates[-1], 
            periods=self.h+1, freq=frequency).values, 0).tolist()  
        
        df_dates = pd.DataFrame({'date': output_dates})
        output_dates = pd.to_datetime(df_dates['date']).dt.date                                

        # obtain time series forecast -----

        input_series = df.drop(columns=['date']).values
        y = stats.ts(FloatVector([item for sublist in input_series.tolist() for item in sublist]))
        self.fcast = ahead.dynrmf(y, h=self.h, level=self.level, pi=self.pi)        


        # result -----

        if (self.date_formatting == "original"): 
            fcast_dates = [datetime.strftime(output_dates[i], "%Y-%m-%d") for i in range(self.h)]            
            self.averages = [[fcast_dates[i], self.fcast.rx2['mean'][i]] for i in range(self.h)]
            self.ranges = [[fcast_dates[i], self.fcast.rx2['lower'][i], self.fcast.rx2['upper'][i]] for i in range(self.h)]            
            return self         
        
        if (self.date_formatting == "ms"):  
            fcast_dates_ms = [int(datetime.strptime(str(output_dates[i]), "%Y-%m-%d").timestamp()*1000) for i in range(self.h)]
            self.averages = [[fcast_dates_ms[i], self.fcast.rx2['mean'][i]] for i in range(self.h)]
            self.ranges = [[fcast_dates_ms[i], self.fcast.rx2['lower'][i], self.fcast.rx2['upper'][i]] for i in range(self.h)]        
            return self         

