# Helper Function for all necessary functions

import os
import sys
import requests

def loadPaths():
    import logging
    file_path = os.path.abspath(__file__)
    directory_path = file_path[:file_path.rfind("/")]
    modules_path = os.path.join(directory_path, "modules")

    if os.path.exists(modules_path):
        sys.path.append(directory_path)    
        sys.path.append(modules_path)
    
    else:
        # Modules not Present
        print("Modules Not Present")
        exit()
    
    print("Modules loaded into sys")

def readFile(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, encoding="utf-8", mode='r') as _file:
                return _file.read()
        else:
            return None
    
    except Exception as _e:
        return None

def cityToCoordinates(cityname):
    apikey = "pk.02b5994cb8a776ef80fd220a5ebd8be4"  # Api key for location iq
    base_url = r"https://us1.locationiq.com/v1/search"
    params = {'key': apikey, 'q': cityname, 'format': 'json'}
    coordinates = None
    try:
        resp = requests.get(base_url, params=params)
        data = resp.json()
        status_code = resp.status_code
        if status_code == 200:
            # API KEY is still valid
            coordinates = (float(data[0]["lat"]), float(data[0]["lon"]))
            # print(coordinates)
        elif status_code == 401:
            print("API Exhausted  while converting City to Coordinates")
            # Write in a log
        
    except Exception as _e:
        print(f"Unknown Error while converting City to Coordiant\n Error : {_e}")
    
    finally:
        return coordinates

def coordinatesToCity(lat, lng):
    apikey = "bdc_43e7339ecac34660a139e16f7073a6ce"  # bigdata-api
    base_url = r"https://api-bdc.net/data/reverse-geocode"
    params = {'latitude': lat, 'longitude': lng, 'localityLanguage': 'en', 'key': apikey}
    city = None
    try:
        resp = requests.get(base_url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            city = data['city']
        elif status_code == 401:
            print("API-BDC API Key Exhausted")
        
    except Exception as _e:
        print(f"Unknown Error\n Error: {_e}")

    finally:
        if city == 'Vishakhapatnam':
            city = "Visakhapatnam"
        return city

def fetchData(lat: float, lng: float):    # This method will be invoked only when user requests resources
    # The lat & lng will not be None
    details = None
    city = coordinatesToCity(lat, lng)
    print(city)
    if city:
        from data import dataStore
        # We need the updated dataStore
        if city in dataStore:
            details = dataStore[city]
        else:
            newcity = newCity(city)
            if newcity is not None:
                print("New CIty created")
                dataStore[city] = newcity
                from earthquake import updateEarthquakeAlerts
                updateEarthquakeAlerts([city])
                # Similarly we will do it for Acuweather API
                from accuweather import fetchWeatherUpdates
                fetchWeatherUpdates([city])
                # Now we can fetch the results from the dataStore
                details = dataStore[city]
            
            else:
                # Unable to create a new city
                print("New CIty not created")
                pass
    
    return parseResults(details)

def newCity(city):
    city_coordinates = cityToCoordinates(city)
    if city_coordinates is not None:
        return {
            "city-coordinates": city_coordinates,
            "numberofalerts": 0,
            "alert_level": 0,
            "alerts": []
        }
    
    return None

def parseResults(details):
    from model import ClientResponse
    if details is None:
        response = ClientResponse(city_coordinates=(0.0, 0.0), alert_level=-1, number_of_alerts=0,
            alerts=["We are unable to fetch your data"])
    
    # Modify the response from the details that will be provided
    else:
        response = ClientResponse(city_coordinates=details["city-coordinates"],
            alert_level=details["alert_level"], number_of_alerts = details["numberofalerts"],
            alerts=[i[1] for i in details["alerts"]])
    
    return response

def updateAlerts():
    # Update & Remove any unused alerts
    from data import dataStore
    cities = list(dataStore.keys())
    # We need to update earthquake results & accuweather results
    pass

def clearAlerts():
    from data import dataStore
    import time
    now_time = time.time()
    for city in dataStore:
        length = number_of_alerts; i = 0
        while i < length:
            if dataStore[city]["alerts"][0] >= now_time:
                # The remove after has expired
                dataStore[city]["alerts"].pop(i)
                continue
            i += 1
        dataStore[city]["numberofalerts"] = len(dataStore[city]["alerts"])
    
    # print("Cleared the Data")


