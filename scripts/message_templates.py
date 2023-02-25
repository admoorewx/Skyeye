import re, datetime

def readable_time(time_string,full_date=False):
	#2023-01-07T18:26:00-06:00
	time_string = time_string[0:-6]
	date_time = datetime.datetime.strptime(time_string,"%Y-%m-%dT%H:%M:%S")
	if date_time.hour == 12:
		hour = 12
		ampm = "PM"
	elif date_time.hour > 12 and date_time.hour <= 23:
		hour = date_time.hour - 12
		ampm = "PM"
	else: 
		hour = date_time.hour
		ampm = "AM"

	if full_date:
		readable = f'{date_time.month}/{date_time.day}/{date_time.year} {hour}:{date_time.minute} {ampm}'
	else:
		readable = f'{hour}:{date_time.minute} {ampm}'
	return readable

def parse_desc(description):
	parts = description.split("\n\n")
	for part in parts: 
		if "HAZARD" in part: 
			hazard = part
		if "SOURCE" in part: 
			source = part 
		if "IMPACT" in part: 
			impact = part 
		if "locations" in part: 
			if "*" in part: 
				locations = part[2:]
			else:
				locations = part 
	return [hazard,source,impact,locations] 

def tor_intensity_by_desc(headline, description):
	if re.search('tornado emergency', headline, re.IGNORECASE):
		return "This is a TORNADO EMERGENCY! You are in a life threatening situation!\n\n"
	elif re.search('particularly dangerous', description, re.IGNORECASE):
		return "This is a Particularly Dangerous Situation!\n\n"
	else: 
		return ""

def wfo_from_vtec(vtec):
	parts = vtec.split(".")
	wfo = parts[2]
	wfo = wfo[1:] # Remove the "K". Example: KOUN => OUN
	return wfo

def new_severe_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	desc_parts = parse_desc(alert['properties']['description'])
	headline = alert['properties']['headline']
	message = f'Sky Eye Weather Alert:\n' \
			  f'{headline} for your location.\n\n'\
			  f'{desc_parts[0]}\n' \
			  f'{desc_parts[1]}\n' \
			  f'{desc_parts[2]}\n\n' \
			  f'Additional details:\n' \
			  f'{desc_parts[3]}\n' \
			  f'For more information go to www.weather.gov/{wfo}.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com'
	return message

def con_severe_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	desc_parts = alert['properties']['description'].split("\n\n")
	headline = alert['properties']['headline']
	endtime = readable_time(alert['properties']['ends'])
	message = f'Sky Eye Weather Alert:\n' \
			  f'A Severe Thunderstorm Warning continues for your location until {endtime}.\n\n'\
			  f'{desc_parts[0]}\n' \
			  f'{desc_parts[1]}\n' \
			  f'{desc_parts[2]}\n\n' \
			  f'Additional details:\n' \
			  f'{desc_parts[3]}\n' \
			  f'For more information go to www.weather.gov/{wfo}.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com'
	return message

def can_severe_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	message = f'Sky Eye Weather Alert:\n' \
			  f'The Severe Thunderstorm Warning for your location has been canceled.\n'\
			  f'Your location is no longer under a severe thunderstorm warning.\n\n'\
			  f'For more information go to www.weather.gov/{wfo}.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com.'
	return message

def exp_severe_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	message = f'Sky Eye Weather Alert:\n' \
			  f'The Severe Thunderstorm Warning for your location has expired.\n'\
			  f'Your location is no longer under a severe thunderstorm warning.\n\n'\
			  f'For more information go to www.weather.gov/{wfo}.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com.'
	return message

def new_tor_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	desc_parts = parse_desc(alert['properties']['description'])
	headline = alert['properties']['headline']
	tor_intensity = tor_intensity_by_desc(headline,alert['properties']['description'])
	message = f'Sky Eye Weather Alert:\n' \
			  f'{headline} for your location.\n\n'\
			  f'{tor_intensity}'\
			  f'{desc_parts[0]}\n' \
			  f'{desc_parts[1]}\n' \
			  f'{desc_parts[2]}\n\n' \
			  f'Additional details:\n' \
			  f'{desc_parts[3]}\n' \
			  f'Tune to local TV or radio stations for more localized information\n\n'\
			  f'For more information go to www.weather.gov/{wfo}.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com'
	return message

def con_tor_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	desc_parts = parse_desc(alert['properties']['description'])
	headline = alert['properties']['headline']
	tor_intensity = tor_intensity_by_desc(headline,alert['properties']['description'])
	message = f'Sky Eye Weather Alert:\n' \
			  f'{headline} for your location.\n\n'\
			  f'{tor_intensity}'\
			  f'{desc_parts[0]}\n' \
			  f'{desc_parts[1]}\n' \
			  f'{desc_parts[2]}\n\n' \
			  f'Additional details:\n' \
			  f'{desc_parts[3]}\n' \
			  f'Tune to local TV or radio stations for more localized information, \n'\
			  f'or go to www.weather.gov/{wfo}.\n\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com'
	return message

def can_tor_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	message = f'Sky Eye Weather Alert:\n' \
			  f'The Tornado Warning for your location has been canceled.\n'\
			  f'Your location is no longer under a tornado warning.\n\n'\
			  f'{alert["properties"]["description"]}\n\n'\
			  f'For more information go to www.weather.gov/{wfo}.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com.'
	return message

def exp_tor_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	message = f'Sky Eye Weather Alert:\n' \
			  f'The Tornado Warning for your location has been allowed to expire.\n'\
			  f'Your location is no longer under a tornado warning.\n\n'\
			  f'{alert["properties"]["description"]}\n\n'\
			  f'For more information go to www.weather.gov/{wfo}.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com.'
	return message


def new_ff_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	desc_parts = parse_desc(alert['properties']['description'])
	headline = alert['properties']['headline']
	message = f'Sky Eye Weather Alert:\n' \
			  f'{headline} for your location.\n\n'\
			  f'{desc_parts[0]}\n' \
			  f'{desc_parts[1]}\n' \
			  f'{desc_parts[2]}\n' \
			  f'Remember: driving over flooded roads is the\n'\
			  f'greatest hazard to life during a flash flood.\n'\
			  f'Do not drive over water-cover roads!\n\n'\
			  f'Additional details:\n' \
			  f'{desc_parts[3]}\n' \
			  f'For more information go to www.weather.gov/{wfo}\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com'
	return message

def con_ff_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	desc_parts = parse_desc(alert['properties']['description'])
	headline = alert['properties']['headline']
	message = f'Sky Eye Weather Alert:\n' \
			  f'{headline} for your location.\n\n'\
			  f'{desc_parts[0]}\n' \
			  f'{desc_parts[1]}\n' \
			  f'{desc_parts[2]}\n' \
			  f'Remember: driving over flooded roads is the\n'\
			  f'greatest hazard to life during a flash flood.\n'\
			  f'Do not drive over water-cover roads!\n\n'\
			  f'Additional details:\n' \
			  f'{desc_parts[3]}\n' \
			  f'For more information go to www.weather.gov/{wfo}\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com'
	return message

def can_ff_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	message = f'Sky Eye Weather Alert:\n' \
			  f'The Flash Flood Warning for your location has been canceled.\n'\
			  f'Your location is no longer under a Flash Flood Warning.\n\n'\
			  f'NOTE: Some low-lying roads may still be under water.\n'\
			  f'Do not drive across flooded roads!\n\n'\
			  f'For more information go to www.weather.gov/{wfo}.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com.'
	return message

def exp_ff_template(alert):
	wfo = wfo_from_vtec(alert['properties']['parameters']['VTEC'][0])
	message = f'Sky Eye Weather Alert:\n' \
			  f'The Flash Flood Warning for your location has been allowed to expire.\n'\
			  f'Your location is no longer under a Flash Flood Warning.\n\n'\
			  f'NOTE: Some low-lying roads may still be under water.\n'\
			  f'Do not drive across flooded roads!\n\n'\
			  f'For more information go to www.weather.gov/{wfo}.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com.'
	return message

def test_message():
	message = f'Sky Eye Weather Message:\n' \
			  f'This is a test message from the National Weather Service\n'\
			  f'No action is necessary.\n'\
			  f'To opt out of these messages or change your\n'\
			  f'settings, log in to www.skyeye.com.'
	return message 

def parse_alert(alert):
	vtec = alert['properties']['parameters']['VTEC'][0]
	if "TEST" in vtec:
		message = test_message()
	elif "SV" in vtec:
		if "NEW" in vtec: 
			message = new_severe_template(alert)
		elif "CON" in vtec: 
			message = con_severe_template(alert)
		elif "CAN": 
			message = can_severe_template(alert)
		else: 
			message = exp_severe_template(alert)
	elif "TO" in vtec: 
		if "NEW" in vtec: 
			message = new_tor_template(alert)
		elif "CON" in vtec: 
			message = con_tor_template(alert)
		elif "CAN": 
			message = can_tor_template(alert)
		else: 
			message = exp_tor_template(alert)
	elif "FF" in vtec: 
		if "NEW" in vtec: 
			message = new_ff_template(alert)
		elif "CON" in vtec: 
			message = con_ff_template(alert)
		elif "CAN": 
			message = can_ff_template(alert)
		else: 
			message = exp_ff_template(alert)
	else: 
		#print(alert['properties']['description'])
		message = None
	return message
