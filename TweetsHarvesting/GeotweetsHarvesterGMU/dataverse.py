from datetime import datetime
import json
import time
import os
import requests  # http://docs.python-requests.org/en/master/

# --------------------------------------------------
# Update the 3 params below to run this code
# --------------------------------------------------

dataverse_server = 'https://dataverse.massopen.cloud' # no trailing slash
api_key = '0ae70426-f205-4256-9763-f936b0fd43bf'
#dataset_id = 1  # database id of the dataset
persistentId = 'doi:10.5072/FK2/UXPC8I' # doi or hdl of the dataset

#dataverse_id = "geo-tweets" #database id of the dataverse
# Using a "jsonData" parameter, add description for dataset
#drname='/Users/Happy/Desktop/json/'
dirname='/home/ubuntu/geo_tweets_harvester/data/'
#dirname='/Users/Happy/Desktop/geo/'
# --------------------------------------------------
# Add file using the Dataset's persistentId (e.g. doi, hdl, etc)
# --------------------------------------------------
url_persistent_id = '%s/api/datasets/:persistentId/add?persistentId=%s&key=%s' % (dataverse_server, persistentId, api_key)

date= datetime.now().strftime('%Y-%m-%d %H')
year = date[:4]
month= date[5:7]
day= date[8:10]
hour=date[11:13]
DHG = year + '_' + month + '_' + day + '_' + hour
fnameold = "geo_tweets_hour_" + DHG + ".tsv"

# --------------------------------------------------
# Using a "jsonData" parameter, add optional description + file tags
# --------------------------------------------------
params = dict(description='tweets',
            categories=['twitter', 'Geo'])

params_as_json_string = json.dumps(params)

payload = dict(jsonData=params_as_json_string)

for fname in os.listdir(dirname):
    print(fname)
    time.sleep(60)
    if (fname == fnameold):
        continue
    else:
        files = {'file': open(os.path.join(dirname, fname), 'rb')}

        # -------------------
        # Make the request
        # -------------------
        print('-' * 40)
        print('making request: %s' % url_persistent_id)
        try:
            r = requests.post(url_persistent_id, data=payload, files=files)
            result = r.json()
            
            #print(result['status'])
            if(result['status'] != 'OK'):
               # r = requests.post(url_persistent_id, data=payload, files=files)
               # result = r.json()
               print(result['status'])
               #  os.remove(os.path.join(dirname,fname))
                


     #       os.remove(os.path.join(dirname, fname))

            # -------------------
            # Print the response
            # -------------------
            print('-' * 40)
            print(r.json())
            print(r.status_code)
        except Exception as x:
            print("Error sending file:",x)
      
