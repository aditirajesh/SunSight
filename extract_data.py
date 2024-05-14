import schedule
import time 
import requests 
from datetime import date,timedelta

def request_data():
    api_key = "YOUR API KEY"
    latitude = 13.082680
    longitude = 80.270721
    today = date.today()
    interval  = "15m"  #15 minute intervals

    url_irradiance = "https://api.openweathermap.org/energy/1.0/solar/interval_data?lat={}&lon={}&date={}&interval={}&tz=+05:30&appid={}".format(latitude,longitude,today,interval,api_key)
    url_temperature = "http://api.openweathermap.org/data/2.5/weather?appid={}&q={}".format(api_key,'chennai')
    print(url_irradiance)
    print(url_temperature)

    response = requests.get(url_irradiance)
    data = response.json()
    irradiation_today = data['irradiance']['daily']
    data_irradiance = irradiation_today[0]['cloudy_sky']['dni']

    response2 = requests.get(url_temperature)
    data2 = response2.json() 
    data_temperature = data2["main"]["temp"] - 273.15


    module_temperature = data_temperature + ((30/800)*(abs(data_irradiance-800)))

    return [data_temperature,module_temperature,data_irradiance]

if __name__ == '__main__':
    print(request_data())
