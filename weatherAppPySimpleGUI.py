# Aseem Timalsina
# c0839829

# use 'py c0839829.py' to run the program. Using 'python c0839829.py'
# may cause error.

import PySimpleGUI as sg
import pyowm
import time
import requests

owmKey = 'b5d209875bb6f3608c6d42b2f6609e31' # API key
weatherDataDict = {} 

def getWeatherStats(city):
	owm = pyowm.OWM(owmKey)
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place(city)
	w = observation.weather
	windSpeed = w.wind(unit='miles_hour')
	pressure = w.barometric_pressure()
	tempC = w.temperature('celsius')
	tempF = w.temperature('fahrenheit')
	status = w.detailed_status
	icon = 'http://openweathermap.org/img/wn/' + w.weather_icon_name + '@2x.png'
	# https://github.com/PySimpleGUI/PySimpleGUI/issues/2941
	response = requests.get(icon, stream=True)
	response.raw.decode_content = True
	# assign every data of weather to weatherDataDict
	weatherDataDict["tempC"] = str(int(tempC['temp']))
	weatherDataDict["tempF"] = str(int(tempF['temp']))
	weatherDataDict["status"] = "Status: " + status
	weatherDataDict["windSpeed"] = "Wind: " + str(int(windSpeed['speed'])) + "m/h"
	weatherDataDict["pressure"] = "Pressure: " + str(int(pressure['press'])) + "hPa"
	weatherDataDict["icon"] = response.raw.read()
	print(w.weather_icon_name)
	return weatherDataDict

# default city
getWeatherStats('Sarnia')
# Define the window's contents
layout = [[sg.Text("Enter a city: ", font='Halvetica 15 bold')],
		  [sg.Input('Sarnia', key='-INPUT-', size=(20,1), font='Halvetica 20 bold'), sg.Button('Search', button_color=('white','#5e9e2e'), font='Halvetica 15')],
		  [sg.Image(weatherDataDict["icon"], size=(70,80))],
		  [sg.Text(weatherDataDict["tempC"] + u'\N{DEGREE SIGN}C / ' + weatherDataDict["tempF"] + u'\N{DEGREE SIGN}F', font='Halvetica 25 bold', text_color='#c9869a', key=1)],
		  [sg.Text(weatherDataDict["status"], font='Halvetica 15 bold', text_color='#6D435A', key=2)], # for status
		  [sg.Text(weatherDataDict["windSpeed"], font='Halvetica 15 bold', text_color='#B17A83', key=3)], # for wind speed
		  [sg.Text(weatherDataDict["pressure"], font='Halvetica 15', text_color='#A99688', key=4)], # for pressure
		  [sg.Text('Stats will refresh when timer reaches 30 mins',font='Halvetica 10')], # label for timer
		  [sg.Text(size=(8,2), font='Halvetica 15 bold', text_color='dark red', key=5)], # for timer
		  [sg.Button('Quit', button_color=('white','#ba382f'), font='Halvetica 15')]]

# Create the window
window = sg.Window('Pitter Patter', layout, element_justification='c')

current_time = 0
start_time = int(round(time.time() * 100))
end_time = time.time() + 1800 # 1800 seconds is 30 mins
	
# Display and interact with the Window using an Event Loop
while True:
	event, values = window.read(timeout=10) # timeout in 10 milliseconds
	current_time = int(round(time.time() * 100)) - start_time
	# See if user wants to quit or window was closed
	if event == sg.WINDOW_CLOSED or event == 'Quit':
		break
	# Update stats when user clicks search button
	if event == 'Search':
		getWeatherStats(values['-INPUT-'])
		start_time = int(round(time.time() * 100))
		current_time =  int(round(time.time() * 100)) - start_time
		end_time = time.time() + 1800
		window[0].update(weatherDataDict["icon"]),
		window[1].update(weatherDataDict["tempC"] + u'\N{DEGREE SIGN}C / ' 	+ weatherDataDict["tempF"] + u'\N{DEGREE SIGN}F'),
		window[2].update(weatherDataDict["status"]),
		window[3].update(weatherDataDict["windSpeed"]),
		window[4].update(weatherDataDict["pressure"])
	
	if (time.time() > end_time):
		getWeatherStats(values['-INPUT-'])
		start_time = int(round(time.time() * 100))
		current_time =  int(round(time.time() * 100)) - start_time
		end_time = time.time() + 1800
		window[0].update(weatherDataDict["icon"]),
		window[1].update(weatherDataDict["tempC"] + u'\N{DEGREE SIGN}C / ' 	+ weatherDataDict["tempF"] + u'\N{DEGREE SIGN}F'),
		window[2].update(weatherDataDict["status"]),
		window[3].update(weatherDataDict["windSpeed"]),
		window[4].update(weatherDataDict["pressure"])
	# Update timer	
	window[5].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
													(current_time // 100) % 60,current_time % 100))
	
# Finish up by removing from the screen
window.close()