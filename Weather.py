import requests
from pprint import pprint
from datetime import datetime
from dateutil import tz
import clipboard
import credentials

wu_key = credentials.wu_key

url = "http://api.wunderground.com/api/"+wu_key+"/conditions/q/VT/Essex.json"
dataset = requests.get(url).json()

temp = str(dataset['current_observation']['temp_f'])+" F"
conditions = dataset['current_observation']['weather']
windchill = str(dataset['current_observation']['windchill_f'])+" F"
feels_like = str(dataset['current_observation']['feelslike_f'])+" F"
wind = str(dataset['current_observation']['wind_mph'])+" MPH"

pprint(dataset)

w = []
#w.append("\n")
w.append("Weather:")
w.append("\n   Temp: " +temp)
w.append("\n   Windchill: " +windchill)
w.append("\n   Feels Like: " +feels_like)
w.append("\n   Wind Speed: " +wind)
w.append("\n   Conditions: " +conditions)

weather = ''.join(w)

data = weather
data_bytes = data.encode("utf-8")

clipboard.copy(data_bytes)
