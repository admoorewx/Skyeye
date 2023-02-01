import datetime
import itertools
import numpy as np
from SMS import send_message
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from nws_warnings import retrieve_last_alerts
from retrieve_profile import *
from message_templates import parse_alert


def get_alert_expiration_time(alert):
	time_string = alert['properties']['ends']
	#2023-01-07T18:26:00-06:00
	timezone_adjustment = time_string[-5:-3]
	time_string = time_string[0:-6]
	local_exp_time = datetime.datetime.strptime(time_string,"%Y-%m-%dT%H:%M:%S")
	utc_exp_time = local_exp_time + datetime.timedelta(hours=int(timezone_adjustment))
	return local_exp_time,utc_exp_time

def reverse_latlon_tuple(latlon):
	return (latlon[1],latlon[0])


# Set the message counter 
sms_counter = 0

# Start by getting the latest 5 warnings
number_of_warnings = 5
alerts = retrieve_last_alerts(number_of_warnings)

# Keep only the warnings with geometries for now
keep_inds = []
now = datetime.datetime.utcnow()
for i, alert in enumerate(alerts):
	#print(alert['properties']['headline'])
	if alert['geometry'] is not None:
		if alert['properties']['ends'] is not None:
			local_exp_time, utc_exp_time = get_alert_expiration_time(alert)
			# Keep only the warnings that fall within the time limit
			if now < utc_exp_time:
				keep_inds.append(i)
				parse_alert(alert)

alerts = np.asarray(alerts)[keep_inds]

# Create polygons based on the alert geometries
polygons = []
for alert in alerts: 
	vertices = np.asarray(alert['geometry']['coordinates']).squeeze()
	points = [(v[0],v[1]) for v in vertices]
	polygon = Polygon(points)
	polygons.append(polygon)

# Get all profile/user lat/lon points
user_info = get_all_profile_info()

# Convert lat/lons to shapely Points and determine
# if it's in a polygon
for user in user_info:
	point = Point(user[3],user[2])
	for i, polygon in enumerate(polygons):
		if polygon.contains(point):
			print("Sending message!")
			carrier = user[5]
			number = user[1]
			message = parse_alert(alerts[i])
			sms_counter = sms_counter + 1
			# Send SMS message
			# send_message(number,carrier,message)

print(f'Complete. Sent a total of {sms_counter} messages.')