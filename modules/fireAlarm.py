# This is the fire alarm module

import time

def fetchSensorMetadata(sesnor_id):
    # Fetch sensor metadata from the db and return city name
    return 'Visakhapatnam'

def updateFireAlerts(sensor_id: int, city: str=None):
    from data import dataStore
    if city is None:
        city = fetchSensorMetadata(sensor_id)  # Fetches sensor data by querying the database, for now disabled
    
    if city is not None:
        if city not in dataStore:
            from helper import newCity
            newcity = newCity(city)
            if newcity is not None:
                dataStore[city] = newcity
            else:
                return None
            
        now_time = time.time()
        from model import Alert
        # print("Fire City", city)
        alert = Alert(city = city, alert_level = 3, message = f"A Forest Fire has been detected at {city}. Take necessary precautions",
            disaster="Forest Fire", remove_after=now_time+15)
        
        from dataproc import updateDataStore
        updateDataStore([alert])
        # print(f"Updated Fire Alert at - {city}")
    