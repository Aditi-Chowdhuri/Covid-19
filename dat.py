import pandas as pd 
import numpy as np
import tensorflow as tf
import datetime

gpus=tf.config.experimental.get_visible_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

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

        self.daily_confirmed_country=self.confirmed_country.copy()
        for i in range(len(self.dates)-1, 0, -1):
            self.daily_confirmed_country[self.dates[i]]=self.daily_confirmed_country[self.dates[i]]-self.daily_confirmed_country[self.dates[i-1]]
        self.model = tf.keras.models.load_model("model/world_model.h5")
        self.max = 360934
        self.temp = np.float32(self.daily_confirmed_country.iloc[-1,-10:].values/439890.0)
        self.p = self.model.predict(np.reshape(self.temp, (1, -1, 1)))[0][0]
        for i in range(9):
            self.temp = np.append(self.temp, self.p)[1:]
            self.p = self.model.predict(np.reshape(self.temp, (1, -1, 1)))[0][0]
        self.temp*=360934
    
    def get_total_confirm(self, cntry):
        if cntry=="World":
            temp=-1
        else:
            temp=np.where(self.countries == cntry)[0][0]
        self.tots=np.uint32(self.confirmed_country.iloc[temp,1:].values)
        self.totdat=dict()
        for i in range(self.dates.shape[0]):
            self.cd="20"+self.dates[i][-2:]+"/"+self.dates[i][:-3]
            self.totdat[self.cd]=self.tots[i]
        return str({"confirmed":self.totdat}).replace("\'","\"").replace("/","-")
    
    def get_total_deaths(self, cntry):
        if cntry=="World":
            temp=-1
        else:
            temp=np.where(self.countries == cntry)[0][0]
        self.tots=np.uint32(self.deaths_country.iloc[temp,1:].values)
        self.totdat=dict()
        for i in range(self.dates.shape[0]):
            self.cd="20"+self.dates[i][-2:]+"/"+self.dates[i][:-3]
            self.totdat[self.cd]=self.tots[i]
        return str({"deaths":self.totdat}).replace("\'","\"").replace("/","-")

    def get_total_recov(self, cntry):
        if cntry=="World":
            temp=-1
        else:
            temp=np.where(self.countries == cntry)[0][0]
        self.tots=np.uint32(self.recovered_country.iloc[temp,1:].values)
        self.totdat=dict()
        for i in range(self.dates.shape[0]):
            self.cd="20"+self.dates[i][-2:]+"/"+self.dates[i][:-3]
            self.totdat[self.cd]=self.tots[i]
        return str({"recovered":self.totdat}).replace("\'","\"").replace("/","-")

    def get_daily_confirmed_world(self, cntry):
        if cntry=="World":
            temp=-1
        else:
            temp=np.where(self.countries == cntry)[0][0]
        self.tots=np.uint32(self.daily_confirmed_country.iloc[temp,1:].values)
        self.totdat=dict()
        for i in range(self.dates.shape[0]):
            self.cd="20"+self.dates[i][-2:]+"/"+self.dates[i][:-3]
            self.totdat[self.cd]=self.tots[i]
        if cntry=="World":
            return str({"daily_confirm":self.totdat, "pred": self.get_world_pred()}).replace("\'","\"").replace("/","-")
        return str({"daily_confirm":self.totdat}).replace("\'","\"").replace("/","-")

    def get_world_pred(self):
        self.cd="20"+self.dates[-1][-2:]+"/"+self.dates[-1][:-3]
        print(self.cd)
        self.totdat=dict()
        for i in range(10):
            self.totdat[self.cd]=self.temp[i]
            self.cd = self.nextday(self.cd)
        return self.totdat
    
    def nextday(self, a):
        a=a.split('/')
        y = int(a[0])
        m = int(a[1])
        d = int(a[2])+1
        if m==2:
            if y%4==0 and y%100!=0 or y%400==0:
                m+=d//30
                d%=29
                if d==0:
                    d=29
            else:
                m+=d//29
                d%=28
                if d==0:
                    d=28
        elif m in [1, 3, 5, 7, 8, 10, 12]:
            m+=d//32
            d%=31
            if d==0:
                d=31
        else:
            m+=d//31
            d%=30
            if d==0:
                d=30
        y+=m//13
        m%=12
        if m==0:
            m=12
        return "%d/%d/%d"%(y, m, d)
