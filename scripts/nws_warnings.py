import json
import requests

def get_alerts():
	url = "https://api.weather.gov/alerts/active"
	response = requests.get(url)
	alerts = response.json()['features']
	return alerts

def retrieve_latest_alert():
	alerts = get_alerts()
	last_alert = alerts[-1]
	return last_alert

def retrieve_last_alerts(number_of_alerts):
	alerts = get_alerts()
	return alerts[0:number_of_alerts]