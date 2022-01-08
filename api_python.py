from flask import Flask
from flask_restful import Api, Resource
import requests
import geocoder
import json
app = Flask(__name__)
api = Api(app)


data = {"current_temp": "", "fahrenheit" : "",}


def getData():
        # base URL
        BASE_URL = "https://api.openweathermap.org/data/2.5/find?"
        g = geocoder.ip('me')
        location = g.latlng
        print(location)
        LATITUDE = str(location[0])
        LONGITUDE = str(location[1])
        API_KEY = "d52359a726a667d5d467466633f50923"
        # upadting the URL
        URL = BASE_URL + "lat=" + LATITUDE + "&lon=" + LONGITUDE + "&appid=" + API_KEY
        # HTTP request
        response = requests.get(URL)
        # checking the status code of the request 
        if response.status_code == 200:
            weather_data = response.json()
            list1 = weather_data['list']
            main = list1[0]
            s = main['main']
            temp_kelvin = s['temp']
            data["current_temp"] = round(temp_kelvin - 273.15,2)
            data["humidity"] = s['humidity']
            
        else:
            # showing the error message
            print("Error in the HTTP request")
        degree = data["current_temp"]
        data["fahrenheit"] = (int(degree) * 9/5) + 32
        print(data["fahrenheit"])
        return data

class Current_temp(Resource):
    def get(self):
        data = getData()
        dict_pairs = data.items()
        pairs_iterator = iter(dict_pairs)
        first_pair = next(pairs_iterator)
        second_pair = next(pairs_iterator)
        return json.dumps(first_pair)


class Humidity(Resource):
    def get(self):
        data = getData()
        dict_pairs = data.items()
        pairs_iterator = iter(dict_pairs)
        first_pair = next(pairs_iterator)
        second_pair = next(pairs_iterator)
        third_pair = next(pairs_iterator)
        return json.dumps(third_pair)

api.add_resource(Current_temp, "/AirConditioner/current_temperature")
api.add_resource(Humidity, "/AirConditioner/humidity")

if __name__ == "__main__":
    app.run(debug = True)