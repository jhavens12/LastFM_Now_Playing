import requests
from pprint import pprint
from datetime import datetime
from dateutil import tz
import clipboard

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')

l = []

time = datetime.now()
l.append(str(time.month) +"/"+ str(time.day)+"/"+ str(time.year)+" "+str(time.time().strftime('%I:%M %p')))

lastfm = ''.join(l)
data = lastfm
data_bytes = data.encode("utf-8")

clipboard.copy(data_bytes)
