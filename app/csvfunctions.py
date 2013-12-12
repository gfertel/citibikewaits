from urllib2 import urlopen
from json import load
import csv
import math
import numpy
from datetime import date, datetime, time, timedelta

def build_array():
	import csv
	array = []
	with open("twostations.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			row[0] = datetime.strptime(row[0], "%Y-%m-%d").date()
			row[1] = datetime.strptime(row[1], "%H:%M:%S").time()
			row[2] = int(row[2])
			row[3] = int(row[3])
			row[4] = int(row[4])		
			array.append(list(row))
	return array
	
stationToID = {"E 11 St & 2 Ave":237, "MacDougal St & Prince St": 128}

def query_array(station_id, array, dtm = datetime.now().replace(microsecond=0), mins = 30):
	from datetime import date, datetime, time, timedelta
	data = []
	min_time = (dtm - timedelta(minutes = mins / 2)).time()
	max_time = (dtm + timedelta(minutes = mins + 90)).time()
	wkday = dtm.weekday()
	if wkday in range(0, 5):
		day_range = range(0, 5)
	else:
		day_range = range(5, 7) 
	for row in array:
		if row[1] >= min_time and row[1] <= max_time:
			if row[2] == station_id:
				if row[0].weekday() in day_range:
					data.append(row)
	return data
	
def percentile(N, percent, key=lambda x:x):
	"""
	Find the percentile of a list of values.
	@parameter N - is a list of values. Note N MUST BE already sorted.
	@parameter percent - a float value from 0.0 to 1.0.
	@parameter key - optional key function to compute value from each element of N.
	@return - the percentile of the values
	"""
	if not N:
		return None
	k = (len(N)-1) * percent
	f = math.floor(k)
	c = math.ceil(k)
	if f == c:
		return key(N[int(k)])
	d0 = key(N[int(f)]) * (c-k)
	d1 = key(N[int(c)]) * (k-f)
	return d0+d1

def analyze(array, station_id, mins = 30):
	#(list of lists, int) -> strings summarizing the situation
	dates = set([line[0] for line in array])
	# checks if there are fewer docks or bikes and decides what the user is looking for
	if get_status(station_id)[0] >= get_status(station_id)[1]:
		lookingfor = "You must be looking for a dock."
		col = 4
	
	else:
		lookingfor = "You must be looking for a bike."
		col = 3
	
	waits = []
	# for each minute in our sample, this loop parses through our sample
	# to find the next minute where a bike has been returned/removed
	for date in dates:
		data = [line[col] for line in array if line[0] == date]
		for i in range(mins):
			for n in range(i + 1, len(data)):
				if data[n] > data[i]:
					waits.append(n - i)
					break
				elif data[n] < data[i]:
					data[i] = data[n]

	percentiles = (percentile(sorted(waits), .75), percentile(sorted(waits), .25))
	
	return {'looking': lookingfor, 'median': numpy.median(waits), 'average': round(numpy.mean(waits), 2), 'perc25':percentile(sorted(waits), .25), 'perc75': percentile(sorted(waits), .75)}
	
			
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
