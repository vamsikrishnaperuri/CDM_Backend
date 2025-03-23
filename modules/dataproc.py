# Functions to help with modifying the datastore

def updateDataStore(alerts):
    from data import dataStore
    # print(type(alerts))
    to_call = []    # List of cities
    for alert in alerts:
        flag = True
        city = alert.city
        dataStore[city]["alert_level"] = max(dataStore[city]["alert_level"], alert.alert_level)
        for index, alert_msg in enumerate(dataStore[city]["alerts"]):
            # print(alert_msg[1] == alert.message)
            if alert_msg[1] == alert.message:
                # We have updated the already existing alert
                dataStore[city]["alerts"][index][0] = alert.remove_after
                flag = False
                break
        
        # If the alert is not present then add the alert & update the number of alerts
        if flag is True:
            dataStore[city]["alerts"].append([alert.remove_after, alert.message])
            dataStore[city]["numberofalerts"] = len(dataStore[city]["alerts"])
            to_call.append(f"{alert.disaster} at {alert.city}")
        
        text = "These are the new alerts: " + ", ".join(to_call)
        from call import call
        call(text)
