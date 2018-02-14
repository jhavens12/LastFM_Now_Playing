import requests
from pprint import pprint
from datetime import datetime
from dateutil import tz
import clipboard
import credentials

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')

key = credentials.key
user = credentials.user

url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="+user+"&api_key="+key+"&limit=5&format=json"
dataset = requests.get(url).json()
dict_1 = {}
for n,i in enumerate(dataset['recenttracks']['track']):
    s = n+1
    dict_1[s] = {}
    dict_1[s]['artist'] = i['artist']['#text']
    dict_1[s]['track'] = i['name']
    dict_1[s]['album'] = i['album']['#text']
    if 'date' in i:
        utc_time = datetime.utcfromtimestamp(int(i['date']['uts']))
        utc = utc_time.replace(tzinfo=from_zone)
        eastern = utc.astimezone(to_zone)
        dict_1[s]['time_stamp'] = eastern
    else:
        dict_1[s]['time_stamp'] = "Now Playing"

l = []
track_list = [2,3,4]

if dict_1[1]['time_stamp'] == "Now Playing":
    playing = True
    l.append("Now Playing:")
    time = datetime.now()
    l.append("\n    "+str(time.month) +"/"+ str(time.day)+" "+ str(time.time().strftime('%I:%M %p')))

else:
    playing = False
    l.append("Last Played: ")
    l.append("\n    "+str(dict_1[1]['time_stamp'].month) +"/"+ str(dict_1[1]['time_stamp'].day)+" "+ str(dict_1[1]['time_stamp'].time().strftime('%I:%M %p')))

if dict_1[1]['track'] == dict_1[2]['track']:
    if dict_1[1]['artist'] == dict_1[2]['artist']:
        del dict_1[2]
        track_list = [3,4,5]

l.append("\n        Artist: "+dict_1[1]['artist'])
l.append("\n        Track: "+dict_1[1]['track'])
if dict_1[1]['album'] != '':
    l.append("\n        Album: "+dict_1[1]['album'])
url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key="+key+"&artist="+dict_1[1]['artist']+"&track="+dict_1[1]['track']+"&username="+user+"&format=json"
dataset = requests.get(url).json()
if 'track' in dataset:
    if 'userplaycount' in dataset['track']:
        l.append("\n        Times Listened to: "+dataset['track']['userplaycount'])

l.append("\nPrevious Tracks: ")
for track in track_list:
    l.append("\n    "+str(dict_1[track]['time_stamp'].month) +"/"+ str(dict_1[track]['time_stamp'].day)+" "+ str(dict_1[track]['time_stamp'].time().strftime('%I:%M %p')))
    l.append("\n        Artist: "+dict_1[track]['artist'])
    l.append("\n        Track: "+dict_1[track]['track'])
    if dict_1[track]['album'] != '':
        l.append("\n        Album: "+dict_1[track]['album'])
    url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key="+key+"&artist="+dict_1[track]['artist']+"&track="+dict_1[track]['track']+"&username="+user+"&format=json"
    dataset = requests.get(url).json()
#    if 'track' in dataset:
#        if 'userplaycount' in dataset['track']:
#            l.append("\n        Times Listened to: "+dataset['track']['userplaycount'])

l.append("\n")

# wu_key = credentials.wu_key
#
# url = "http://api.wunderground.com/api/"+wu_key+"/conditions/q/VT/Essex.json"
# dataset = requests.get(url).json()
#
# temp = str(dataset['current_observation']['temp_f'])+" F"
# conditions = dataset['current_observation']['weather']

# w = []
# w.append("\n")
# w.append("Weather:")
# w.append("\n   Temp: " +temp)
# w.append("\n   Conditions: " +conditions)

# weather = ''.join(w)
lastfm = ''.join(l)
data = lastfm#+weather
data_bytes = data.encode("utf-8")

clipboard.copy(data_bytes)
