import pandas as pd 
import numpy as np

class dater:
    def __init__(self):
        self.confirmed=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
        self.deaths=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
        self.recovered=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

        self.confirmed_country = self.confirmed.iloc[:, 1:].groupby(['Country/Region']).sum().iloc[:, 2:].reset_index()
        self.deaths_country = self.deaths.iloc[:, 1:].groupby(['Country/Region']).sum().iloc[:, 2:].reset_index()
        self.recovered_country = self.recovered.iloc[:, 1:].groupby(['Country/Region']).sum().iloc[:, 2:].reset_index()

        self.confirmed_country=self.confirmed_country.append(self.confirmed_country.iloc[:,1:].sum(axis=0), ignore_index=True)
        self.deaths_country=self.deaths_country.append(self.deaths_country.iloc[:,1:].sum(axis=0), ignore_index=True)
        self.recovered_country=self.recovered_country.append(self.recovered_country.iloc[:,1:].sum(axis=0), ignore_index=True)

        self.countries=self.confirmed_country.iloc[:, 0].values
        self.dates=self.confirmed_country.columns.values[1:]

        self.daily_confirmed_country=self.confirmed_country
        for i in range(len(self.dates)-1, 0, -1):
            self.daily_confirmed_country[self.dates[i]]=self.daily_confirmed_country[self.dates[i]]-self.daily_confirmed_country[self.dates[i-1]]
    
    def get_total_confirm(self):
        self.tots=np.uint32(self.confirmed_country.iloc[-1,1:].values)
        self.totdat=dict()
        for i in range(self.dates.shape[0]):
            self.cd="20"+self.dates[i][-2:]+"/"+self.dates[i][:-3]
            self.totdat[self.cd]=self.tots[i]
        return str({"confirmed":self.totdat}).replace("\'","\"").replace("/","-")
    
    def get_total_deaths(self):
        self.tots=np.uint32(self.deaths_country.iloc[-1,1:].values)
        self.totdat=dict()
        for i in range(self.dates.shape[0]):
            self.cd="20"+self.dates[i][-2:]+"/"+self.dates[i][:-3]
            self.totdat[self.cd]=self.tots[i]
        return str({"deaths":self.totdat}).replace("\'","\"").replace("/","-")

    def get_total_recov(self):
        self.tots=np.uint32(self.recovered_country.iloc[-1,1:].values)
        self.totdat=dict()
        for i in range(self.dates.shape[0]):
            self.cd="20"+self.dates[i][-2:]+"/"+self.dates[i][:-3]
            self.totdat[self.cd]=self.tots[i]
        return str({"recovered":self.totdat}).replace("\'","\"").replace("/","-")

    def get_daily_confirmed_world(self):
        self.tots=np.uint32(self.daily_confirmed_country.iloc[-1,1:].values)
        self.totdat=dict()
        for i in range(self.dates.shape[0]):
            self.cd="20"+self.dates[i][-2:]+"/"+self.dates[i][:-3]
            self.totdat[self.cd]=self.tots[i]
        return str({"daily_confirm":self.totdat}).replace("\'","\"").replace("/","-")
