from datetime import datetime
import json
import requests

# Equation to predict clothing with 6:00 AM and indoor temperature
def predict_clothing(sixAmTemp, indoorTemp):
    Icl = 10 ** (0.2134 - 0.0063 * sixAmTemp - 0.0165 * indoorTemp)
    return Icl

#parse the local temperature at 6:00 AM
def parse_temp():
    #Set time as Today at 6:00 AM
    sixAmTime = str(datetime.now().date()) + 'T06:00:00'

    #set API key and location of London Ontario
    API_key = '45b8f20a7e97c59e4ebdd5155b17e065'
    latitude = '42.9833'
    longitude = '-81.2500'

    #Parse 6:00 AM temperature from forecast.io    
    url = 'https://api.forecast.io/forecast/' + API_key + '/' + latitude + ',' + longitude + ',' + sixAmTime
    response = requests.get(url)
    data = json.loads(response.text)

    #convert temperature from fahrenheit to celsius
    temp_F = data['currently']['apparentTemperature']
    temp_C = round((float(temp_F)-32) * (5/9.0),2)


    return temp_C
