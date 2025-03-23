# This module will hold all the data that is common across the project
# No functions must be present in this module

dataStore = dict()
earthquakeData = []

"""
    Format:
        city: {
            'city-coordinates': (lat, lng), 
            'numberofalerts': number,
            'alert_level': (-1, 0, 1, 2, 3, 4),
            'alerts': [alert1, alert2, alert3]  alert:- (remove_after, alert_msg)
        }

    "Visakhapatnam":{
        "city-coordinates": (17.234, 83.412),
        'numberofalerts': 1,
        'alert_level': 1,
        'alerts': [(1739463367.1102438, "There is a Cyclone Alert for your location. Please take precautionary measures")]
    }
"""

    


            
