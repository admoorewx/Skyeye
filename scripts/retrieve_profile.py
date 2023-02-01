import os 
import sqlite3

def database():
	dirname = os.path.dirname(__file__)
	filename = os.path.join(dirname, '../db.sqlite3')
	connection = sqlite3.connect(filename)
	cursor = connection.cursor()
	return connection, cursor

def get_all_profile_info():
	connection, cursor = database()
	cursor.execute("SELECT * FROM profiles_profile")
	profiles = cursor.fetchall()
	connection.close()
	return profiles

def get_all_user_ids():
	connection, cursor = database()
	cursor.execute(f'SELECT user_id FROM profiles_profile')
	response = cursor.fetchall()
	return response

def get_all_latlons():
	connection, cursor = database()
	cursor.execute(f'SELECT lat, lon FROM profiles_profile')
	response = cursor.fetchall()
	return response

def get_all_phones():
	connection, cursor = database()
	cursor.execute(f'SELECT phone FROM profiles_profile')
	response = cursor.fetchall()
	return response

def get_all_carriers():
	connection, cursor = database()
	cursor.execute(f'SELECT carrier FROM profiles_profile')
	response = cursor.fetchall()
	return response

def get_user_latlon(userid):
	connection, cursor = database()
	cursor.execute(f'SELECT lat, lon FROM profiles_profile WHERE user_id = "{userid}"')
	response = cursor.fetchall()
	return response

def get_user_phone(userid):
	connection, cursor = database()
	cursor.execute(f'SELECT phone FROM profiles_profile WHERE user_id = "{userid}"')
	response = cursor.fetchall()
	return response

def get_user_location(userid):
	connection, cursor = database()
	cursor.execute(f'SELECT location_name FROM profiles_profile WHERE user_id = "{user_id}"')
	response = cursor.fectchone()
	return response

def get_all_user_info_as_dict():
	profiles = get_all_profile_info()
	dicts = []
	for prof in profiles:
		prof_dict = {
			"id": prof[0],
			"user_id": prof[5],
			"phone": prof[1],
			"location_name": prof[4],
			"lat": prof[2],
			"lon": prof[3]
		}
		dicts.append(prof_dict)
	return dicts