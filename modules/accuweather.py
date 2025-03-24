# This module is responsible for gathering alerts from Accuweather API

import requests

def fetchWeatherUpdates(cities):
    from model import Alert
    from datetime import datetime
    baseUrl = "http://api.weatherapi.com/v1/alerts.json"
    alerts = []
    for city in cities:
        params = {"key": "ENTER_YOUR_HERE", "q": city}
        response = requests.get(baseUrl, params=params)
        data = response.json()["alerts"]
        for weather_alert in alerts:
            alert = Alert(city=city, alert_level=3, remmove_after=datetime.fromisoformat(data["expires"]), disaster=data["event"], message=data["instruction"])
            alerts.append(alert)
    

    from modules.dataproc import updateDataStore
    updateDataStore(alerts)

def updateWeatherUpdates():
    from data import dataStore
    fetchWeatherUpdates(list(dataStore.keys()))
    # print("Weather Data Updated")


