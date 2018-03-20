# This code harvest NetCDF from NWM website and stores to MOC
# Author:Devika Kakkar
# Modified on: November 21, 2017
# coding: utf-8

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
url = 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/'+ folder +'/analysis_assim/'

# In[13]:

response = urllib.request.urlopen(url)
path_base = "/data/nwm_data"+ "/analysis_assim/"+ yesterday_str
metadata_dict={}
metadata_filename= "metadata_"+ "analysis_assim_"+ yesterday_str+ ".csv"
#os.mkdir(path, 0777)
for lines in response.readlines():
    line_str= lines.decode("utf-8")
    #print(line_str) 
    time_str=['t00','t06','t12','t18']
    
   
    for sub_str in time_str:
        if(sub_str in line_str):
           path = path_base + "/"+ sub_str
           value=os.path.exists(path)
    #print(value)
           if not os.path.exists(path):
              #print("Making directory", path)
              os.makedirs(path)  
           #print(line_str[56:]
           file_time=line_str[50:55]
           #print(file_time)
           index = (line_str.index(".nc"))+3
           filename = line_str[56:index]
           if('land' in filename or (not('tm00' in filename))):
               continue
           else: 
               file_url = url + filename
               local_filename= os.path.join(path, filename)
              # print(local_filename)
              # urllib.request.urlretrieve(file_url,local_filename)
               while True:
                         try:
                              urllib.request.urlretrieve(file_url,local_filename)
                              #print(filename)
                              metadata_dict[filename]=file_time
                              #print(metadata_dict)
                         except urllib.error.URLError as e:
                              print("Error loading file: ", filename)
                              print(e.reason)
                              continue
                         break
                                    
            #print(metadata_dict)
          
            
with open(os.path.join(path_base, metadata_filename),'a+',encoding='utf-8') as myfile:
    wrtr = csv.writer(myfile, delimiter=',', quotechar='"')
    for key in metadata_dict:
        wrtr.writerow([key, metadata_dict[key]])
        myfile.flush() # whenever you want
