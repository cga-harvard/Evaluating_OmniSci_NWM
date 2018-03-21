import boto3
import botocore
import os

BUCKET_NAME = 'national-water-model-data' # replace with your bucket name
model_name='short_range'
date='20171205'
time=['t00','t06','t12','t18']
for timels in time:
       	file_prefix=timels+'z'
        file_suffix=['f006','f012','f018']
        for suffix in file_suffix:
		filename='nwm.'+file_prefix+'.short_range.terrain_rt.'+ suffix + '.conus.nc'
		KEY = model_name+'/'+ date+'/'+ timels+ '/'+ 'nwm.'+ file_prefix+ '.short_range.terrain_rt.'+ suffix + '.conus.nc' # replace with your object key
		s3 = boto3.resource('s3')
		path='/raidStorage/nwm_data/'+ model_name+'/'+date+'/'+timels
		if not os.path.exists(path):
			os.makedirs(path,0755)
		file=path+'/'+filename
        	print(KEY)
		try:
    			s3.Bucket(BUCKET_NAME).download_file(KEY, file)
		except botocore.exceptions.ClientError as e:
    			if e.response['Error']['Code'] == "404":
        			print("The object does not exist.")
    			else:
        			raise
