import os
import datetime
import smtplib
from email.mime.text import MIMEText
date= datetime.datetime.now() - datetime.timedelta(0,3600) #check for file associated with two hours ago- 7200 seconds
date = date.strftime('%Y-%m-%d %H')
year = date[:4]
month= date[5:7]
day= date[8:10]
hour = date[11:13]
DHG = year + '_' + month + '_' + day + '_' + hour
fname = "geo_tweets_hour_" + DHG + ".tsv"
dirname = '/Users/Happy/Desktop/tweets/'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login('bop.harvard@gmail.com','*******') #need to change this to something else?

msg = MIMEText('File missing or less than 1 MB --> ' +'Related Date_Time: ' + DHG )
msg['Subject'] = 'Twitter Harvester Email Alert'
msg['From'] = 'bop.harvard@gmail.com'
msg['To'] = 'devikakakkar29@gmail.com'

file_exists = os.path.isfile(os.path.join(dirname, fname))
if not file_exists:
    server.send_message(msg)
    server.quit()
elif os.stat(os.path.join(dirname, fname)).st_size < 10^6: # if file size < 1MB
    server.send_message(msg)
    server.quit()     
    
