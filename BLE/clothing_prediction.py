from datetime import datetime
import json
import requests

def predict_clothing(sixAmTemp, indoorTemp):
    Icl = 10 ** (0.2134 - 0.0063 * sixAmTemp - 0.0165 * indoorTemp)
    return Icl

def parse_temp():
    sixAmTime = str(datetime.now().date()) + 'T06:00:00'

    API_key = '45b8f20a7e97c59e4ebdd5155b17e065'
    latitude = '42.9833'
    longitude = '-81.2500'

    url = 'https://api.forecast.io/forecast/' + API_key + '/' + latitude + ',' + longitude + ',' + sixAmTime

    response = requests.get(url)

    data = json.loads(response.text)

    #print json.dumps(parsed, indent=4, sort_keys = True)

    temp_F = data['currently']['apparentTemperature']
    temp_C = round((float(temp_F)-32) * (5/9.0),2)


    return temp_C
