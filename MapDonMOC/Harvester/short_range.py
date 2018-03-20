# Import libraries

import urllib.request
import datetime
import os
import csv


# RUn for yesterday

yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
# In[8]: change to str
yesterday_str = (yesterday.strftime('%Y%m%d'))
# In[9]: Define folder name
folder='nwm'+'.'+ yesterday_str
# Find URl for downlaod
url = 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/'+ folder +'/short_range/'

# In[13]:

response = urllib.request.urlopen(url)
path_base = "/data/nwm_data"+ "/short_range/"+ yesterday_str
metadata_dict={}
metadata_filename= "metadata_"+ "short_range_"+ yesterday_str+ ".csv"
#os.mkdir(path, 0777)
for lines in response.readlines():
    line_str= lines.decode("utf-8")
    #print(line_str)
    time_str=['t00','t06','t12','t18']
    for sub_str in time_str:
        if(sub_str in line_str):
           path = path_base+ "/"+ sub_str
           
           value=os.path.exists(path)
    #print(value)
           if not os.path.exists(path):
              #print("Making directory", path)
              os.makedirs(path)  
           #print(line_str[56:]
           file_time=line_str[50:55]
           index = (line_str.index(".nc"))+3
           filename = line_str[56:index]
           #print(filename)
           if(('land' in filename) or (('f006' not in filename) and ('f012' not in filename) and ('f018' not in filename) )):
                       continue
                #print("Not loading file: ", filename)
               
           else: 
               file_url = url + filename
               local_filename= os.path.join(path, filename)
               #print(filename)
               #urllib.request.urlretrieve(file_url,local_filename)
               while True:
                         try:
                              urllib.request.urlretrieve(file_url,local_filename)
                              metadata_dict[filename]=file_time  
                              #print(filename)
                         except urllib.error.URLError as e:
                              print("Error loading file: ", filename)
                              print(e.reason)
                              continue
                         break

            
with open(os.path.join(path_base, metadata_filename),'a+',encoding='utf-8') as myfile:
    wrtr = csv.writer(myfile, delimiter=',', quotechar='"')
    for key in metadata_dict:
        wrtr.writerow([key, metadata_dict[key]])
        myfile.flush() # whenever you want


