import os
import datetime
import smtplib
from email.mime.text import MIMEText
date= datetime.datetime.now() - datetime.timedelta(0,86400) #check for file associated with two hours ago- 7200 seconds
date = date.strftime('%Y-%m-%d %H')
year = date[:4]
month= date[5:7]
day= date[8:10]
hour = date[11:13]
DHG = year  + month  + day 
fname = 'nwm.t18z.medium_range.terrain_rt.f240.conus.nc'
dirname = '/data/nwm_data/medium_range/'+DHG+'/t18/'
#print(dirname)
#filepath=os.path.join(dirname, DHG)
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login('bop.harvard@gmail.com','433633ab') #need to change this to something else?

msg = MIMEText('File missing or less than 1 MB --> '+fname +' Related Date_Time: ' + DHG )
msg['Subject'] = 'NWM Harvester Email Alert'
msg['From'] = 'bop.harvard@gmail.com'
msg['To'] = 'devikakakkar29@gmail.com'

file_exists = os.path.isfile(os.path.join(dirname, fname))
#print(file_exists)
if not file_exists:
    server.send_message(msg)
    server.quit()
elif os.stat(os.path.join(dirname, fname)).st_size < 10^6: # if file size < 1MB
    server.send_message(msg)
    server.quit()
else:
    print("File found", fname)
    
