from urllib2 import urlopen
from json import load

def get_status(station):
	# (str) -> tuple containing current bikes and current docks
	# takes station name and returns current status
	url = "http://api.citybik.es/citibikenyc.json"
	response = urlopen(url)
	data = load(response)
	for i in range(len(data)):
		if data[i]['name'] == station:
			curr_bikes = data[i]['bikes']
			curr_docks = data[i]['free']
			return (curr_bikes, curr_docks)
