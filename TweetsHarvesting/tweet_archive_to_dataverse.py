from datetime import datetime
import json
import os
import requests  # http://docs.python-requests.org/en/master/

# --------------------------------------------------
# Update the 3 params below to run this code
# --------------------------------------------------
dataverse_server = 'https://dataverse.massopen.cloud' # no trailing slash
api_key = '0ae70426-f205-4256-9763-f936b0fd43bf'
dataverse_id = "geo-tweets" #database id of the dataverse 

# --------------------------------------------------
# Using a "jsonData" parameter, add description for dataset
# --------------------------------------------------
with open('dataset.json') as dataset_json_file:
	file = dataset_json_file.read()
data_load = json.loads(file)
data = json.dumps(data_load)

# --------------------------------------------------
# Create new DRAFT dataset in the Harvard CGA Dataverse
# --------------------------------------------------
#curl version
#POST http://$SERVER/api/dataverses/$id/datasets/?key=$apiKey
url_dataverse_id = '%s/api/dataverses/%s/datasets/?key=%s' % (dataverse_server, dataverse_id, api_key)

# -------------------
# Make the request
# -------------------
print('-' * 40)
print('making request: %s' % url_dataverse_id)
r = requests.post(url_dataverse_id, data=data)

# -------------------
# Print the response
# -------------------
print('-' * 40)
print(r.json())
print(r.status_code)

# --------------------------------------------------
# Get id of created dataset
# --------------------------------------------------
dataset_id = r.json()['data']['id'] # database id of the dataset

# --------------------------------------------------
# Prepare "file"
# --------------------------------------------------
#file_content = 'content: %s' % datetime.now()
dirname = 'E:\\2017_Geotweets'
# --------------------------------------------------
# Using a "jsonData" parameter, add optional description + file tags
# --------------------------------------------------
params = dict(description='Tweets',
                categories=['twitter', 'geo'])

params_as_json_string = json.dumps(params)

payload = dict(jsonData=params_as_json_string)

# --------------------------------------------------
# Add file using the Dataset's id
# --------------------------------------------------
# curl version
# POST http://$SERVER/api/datasets/$id/add?key=$apiKey
url_dataset_id = '%s/api/datasets/%s/add?key=%s' % (dataverse_server, dataset_id, api_key)


for fname in os.listdir(dirname):
    print(fname)
    files = {'file': open(os.path.join(dirname, fname), 'rb')}

    # -------------------
    # Make the request
    # -------------------
    print('-' * 40)
    print('making request: %s' % url_dataset_id)
    r = requests.post(url_dataset_id, data=payload, files=files)

    # -------------------
    # Print the response
    # -------------------
    print('-' * 40)
    print(r.json())
    print(r.status_code)

# # --------------------------------------------------
# # Add file using the Dataset's persistentId (e.g. doi, hdl, etc)
# # --------------------------------------------------
# url_persistent_id = '%s/api/datasets/:persistentId/add?persistentId=%s&key=%s' % (dataverse_server, persistentId, api_key)

# # -------------------
# # Update the file content to avoid a duplicate file error
# # -------------------
# file_content = 'content2: %s' % datetime.now()
# files = {'file': ('sample_file2.txt', file_content)}


# # -------------------
# # Make the request
# # -------------------
# print('-' * 40)
# print('making request: %s' % url_persistent_id)
# r = requests.post(url_persistent_id, data=payload, files=files)

# # -------------------
# # Print the response
# # -------------------
# print('-' * 40)
# print(r.json())
# print(r.status_code)
