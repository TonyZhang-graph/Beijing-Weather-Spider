# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 21:56:50 2020

@author: TonyZhang
"""

from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import namedtuple

Website = namedtuple('Website', ['url', 'time_tag', 'weather_tag', 'temp_low_tag', 'temp_high_tag', 'wind_strength_tag'])  
WeatherData = namedtuple('WeatherData', ['time', 'weather', 'temp_low', 'temp_high', 'wind_strength'])

class Weather:
    '''
    储存北京天气
    '''
    def __init__(self, *data):
        self.data = WeatherData(*data)
        
    def __repr__(self):
        return 'time: {}\nweather: {}\ntemp_low: {}\ntemp_high: {}\nwind_strength: {}'.format(*self.data)      
        
class Crawler:
    
    def getPage(self, url):
        try:
            request = Request(url)
            html = urlopen(request)
            bs = BeautifulSoup(html.read(), 'html.parser')
        except:
            return None
        
        return bs
    
    def safeGet(self, bs, selector):
        tags = bs.select(selector)
        if tags is not None:
            values = []
            for tag in tags:
                values.append(tag.get_text())
            return values
        return ''
    
    def crawl(self, website):
        weathers = []
        bs = self.getPage(website.url)
        if bs is not None:
            times = self.safeGet(bs, website.time_tag)
            weas = self.safeGet(bs, website.weather_tag)
            temp_lows = self.safeGet(bs, website.temp_low_tag)
            temp_highs = self.safeGet(bs, website.temp_high_tag)
            wind_strengthes = self.safeGet(bs, website.wind_strength_tag)
            temp_highs.insert(0, '--')
            
            for time, wea, temp_low, temp_high, wind_strength in zip(times, weas, temp_lows, temp_highs, wind_strengthes):
                weather = Weather(time, wea, temp_low, temp_high, wind_strength)
                weathers.append(weather)
                
        return weathers
                

crawler = Crawler()
website_data = ('http://www.weather.com.cn/weather/101010100.shtml', '.t.clearfix li h1', '.t.clearfix li .wea', '.t.clearfix li .tem i', '.t.clearfix li .tem span', '.t.clearfix li p.win i')
website = Website(*website_data)
weathers = crawler.crawl(website)

for each in weathers:
    print('-' * 20)
    print(each)
    
