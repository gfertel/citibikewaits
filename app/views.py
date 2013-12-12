from flask import render_template, flash, redirect
from app import app
from forms import StationForm
from csvfunctions import *

builtarray = build_array()

@app.route('/search', methods = ['GET', 'POST'])
def search():
	form = StationForm()
	if form.validate_on_submit():
		stationID = stationToID[form.station.data]
		response = analyze(query_array(stationID, builtarray), form.station.data)
		flash('Station: ' + form.station.data)
		flash(response['looking'])
		flash('The historical average wait at this time is %d minutes.' % response['average'])
		flash("The historical median wait at this time is %d minutes." % response['median'])
		flash("Fifty percent of the time, waits have been between %(q1)d minutes and %(q3)d minutes." % {"q1": response['perc25'], "q3": response['perc75']})
		return redirect('/search')
	return render_template('search.html', form = form)

@app.route('/')
@app.route('/index')
def index():
	user = { 'nickname': 'Test' }
	return render_template("index.html",
		title = 'Home',
		user = user)

