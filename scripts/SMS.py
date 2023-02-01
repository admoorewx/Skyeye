import smtplib

"""
Relevant documentation for smtplib:
https://docs.python.org/3/library/smtplib.html

- May need to look through this to add additional carriers in the future
"""

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com",
    "boostmobile": "@sms.myboostmobile.com"
}

EMAIL = "skyeyealerts@gmail.com"
PASSWORD = "nbcywjkhqwnyidsn"

def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
    server.sendmail(auth[0], recipient, message)
#send_message("4795979545","att","Get to work!")