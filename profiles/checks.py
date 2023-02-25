import numpy as np

def valid_phone_number(number):
	length = len(str(number))
	if length == 10 or length == 11:
		return True
	else: 
		return False