import requests
from datetime import datetime
import re
import os
import smtplib, ssl
import time
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()


#Variables
peekskillUrl = "https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/branches/1dfcc7900a35932a83e8b05b89d7c67e63a666dc4288bc73262712725787176d/services/ee3480a8232e72e54071cd185388c691f829fa2670e5e6a6f966385908462cb8/dates?_=1615502661885"
whitePlainsUrl = "https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/branches/ee9d5b38b121f0dd4a336a6f36aedff585229808390ebad45860feb74c2d5b63/services/ee3480a8232e72e54071cd185388c691f829fa2670e5e6a6f966385908462cb8/dates?_=1615502661892"
yonkersUrl = "https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/branches/46a32c2d34d1c7719a9e760613f0b7567b34987534a02d5be6cf98c6792a5110/services/ee3480a8232e72e54071cd185388c691f829fa2670e5e6a6f966385908462cb8/dates?_=1615501632541"
#Functions
def checkForEarlierDate(dates, benchmarkDate, location):
    for date in dates:
        dt = datetime.strptime(date, '%Y-%m-%d')
        if (dt < benchmarkDate):
            print("FOUND better date:" + location + ": "+date)
            message = location + ": "+date
            sendNotification(message)

def sendNotification(message):
    smtp_server = os.getenv("SMTP_SERVER")
    port = os.getenv("PORT")
    sender = os.getenv("SENDER")
    password = os.getenv("SENDER_PASSWORD")

    link = "https://nysdmvqw.us.qmatic.cloud/naoa/index.jsp"
    msg = EmailMessage()
    msg.set_content(message + "\n" +link)
    msg['Subject'] = message
    msg['From'] = 'mixedpebble@gmail.com'
    msg['To'] = os.getenv("RECIPIENTS").split(',')


    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(smtp_server, port, context=context)
    server.login(sender, password)
    server.send_message(msg)
    server.quit()

while True:
    # Request Data
    peekskillResponse = requests.request("GET", peekskillUrl, headers={}, data={})
    whitePlainsResponse = requests.request("GET", whitePlainsUrl, headers={}, data={})
    yonkersResponse = requests.request("GET", yonkersUrl, headers={}, data={})

    # Extract dates from Data
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
    peekskillResponse = re.findall(regex, whitePlainsResponse.text)
    whitePlainsDates = re.findall(regex, whitePlainsResponse.text)
    yonkersDates = re.findall(regex, whitePlainsResponse.text)

    # Check for earlier dates & send messages
    benchmarkDate = datetime.strptime(os.getenv("DATE_BENCHMARK"), '%Y-%m-%d')
    checkForEarlierDate(peekskillResponse, benchmarkDate, "peekskill")
    checkForEarlierDate(whitePlainsDates, benchmarkDate, "whiteplanes")
    checkForEarlierDate(yonkersDates, benchmarkDate, "Yonkers")
    sleepTime = int(os.getenv("SLEEP_TIME"))
    time.sleep(sleepTime)




