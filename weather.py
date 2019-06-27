#!/usr/bin/python3

from pprint import pprint
import requests
import time

def gatherData():
    baseurl = "http://api.openweathermap.org/data/2.5/weather?"
    apikey = "f323652442cafdce9ea64fea49a1c573"
    city = "baltimore,us"
    url = baseurl + "appid=" + apikey + "&q=" + city
    r = requests.get(url)
    return r.json()

def formatData(rawWeather):
    city = rawWeather['name']

    tempKelvin = rawWeather['main']['temp']
    tempFahr = (tempKelvin - 273.15) * (9 / 5) + 32
    tempFahr = str(int(tempFahr))

    humidity = str(rawWeather['main']['humidity'])

    pressure = str(rawWeather['main']['pressure'])

    seconds = str(int(time.time()))

    return city + "weather," + "city=" + city + " temp=" + tempFahr + ",humidity=" + humidity + ",pressure=" + pressure + " " + seconds

def sendData(influxData):
# curl -i -XPOST 'http://localhost:8086/write?db=weather&precision=s' --data-binary 'Baltimoreweather,city=Baltimore temp=53,humidity=87,pressure=1010 1557789973'
    api = "http://localhost:8086/write?db=weather&precision=s"
    requests.post(url = api, data = influxData)

rawWeather = gatherData()
influxData = formatData(rawWeather)
sendData(influxData)
