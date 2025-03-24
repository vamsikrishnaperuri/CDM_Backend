# This module deals with managing earthquake data

import math
from model import EarthquakeData
import time

def haversineDistance(coordinate1,coordinate2):
    # Convert latitude and longitude from degrees to radians
    lat1, lng1 = coordinate1
    lat2, lng2 = coordinate2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lng1, lat2, lng2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # Calculate the result
    print("Haversine Distance : ", c * r)
    return c * r

def calculateImpactArea(m):
    if m >= 9.5:
        return 30000
    elif m >= 9.0:
        return 20000
    elif m >= 8.5:
        return 10000
    elif m >= 8.0:
        return 5000
    elif m >= 7.5:
        return 2000
    elif m >= 7.0:
        return 1000
    elif m >= 6.5:
        return 500
    elif m >= 6.0:
        return 400
    elif m >= 5.5:
        return 360
    elif m >= 5.0:
        return 300
    elif m >= 4.5:
        return 200
    elif m >= 4.0:
        return 150
    elif m >= 3.5:
        return 100
    else:
        return 0

def calculateAlertLevel(magnitude):
    if magnitude > 8.5:
        return 4
    elif magnitude > 7:
        return 3
    elif magnitude > 5:
        return 2
    elif magnitude > 3.5:
        return 1
    else:
        return 0

def removeAfter(mag, alert_level):
    now_time = time.time()
    effective_power = mag * alert_level
    return int (now_time + effective_power * 100)

def updateEarthquakeData():
    # This module will only return list of earthquakes that have occured
    url = rf"https://earthquake.usgs.gov/fdsnws/event/1/query"
    from datetime import datetime
    import requests
    params = {'format': 'geojson', 'starttime': str(datetime.now())[:10]}
    resp = requests.get(url=url, params=params, allow_redirects=True)
    data = resp.json()
    if resp.status_code != 200:
        return None
    _earthquake_data = []
    length = len(data["features"])
    now_time = time.time()

    for i in range(length):
        
        eq = EarthquakeData()
        eq.magnitude = data['features'][i]['properties']['mag']
        eq.location = data['features'][i]['properties']['place']
        # print(eq.location)
        _coordinates = data['features'][i]['geometry']['coordinates'][:2]
        eq.coordinates = _coordinates[::-1]
        eq.isTsunami = False if data['features'][i]['properties']['tsunami'] == 0 else True
        eq.time = data['features'][i]['properties']['updated']

        if eq.magnitude < 3.5 and now_time - eq.time > 300:
            pass

        else:
            _earthquake_data.append(eq)
    
    from data import earthquakeData, dataStore
    earthquakeData = _earthquake_data

    # Once we have updated the earthquake data, now we check for alerts in the already present cities
    updateEarthquakeAlerts(list(dataStore.keys()))

def updateEarthquakeAlerts(cities):
    # This is done only if a new city is added
    from data import earthquakeData, dataStore
    alerts = []
    for city in cities:
        for quake in earthquakeData:
            coordinate1 = dataStore[city]['city-coordinates']
            coordinate2 = dataStore[city]['city-coordinates']
            if haversineDistance(coordinate1, coordinate2) <= calculateImpactArea(quake.magnitude):
                alert_level = calculateAlertLevel(quake.magnitude)
                remove_after = removeAfter(alert_level, quake.magnitude)
                disaster = "Tsunami" if quake.isTsunami else "Earthquake"
                alert = Alert(city=city, remove_after=remove_after, 
                    alert_level=alert_level, message="There is an Earthquake at your location. Take Precautions",
                    disaster = disaster)
                alerts.append(alert)
    
    from modules.dataproc import updateDataStore
    updateDataStore(alerts)

