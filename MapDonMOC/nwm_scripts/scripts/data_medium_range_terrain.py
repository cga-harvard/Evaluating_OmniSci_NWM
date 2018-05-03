import boto3
import botocore
import os

BUCKET_NAME = 'national-water-model-data' # replace with your bucket name
model_name='medium_range'
date=['20180101','20180102','20180103','20180104','20180105','20180106','20180107','20180108','20180109','20180110','20180111']
time='t00'
file_suffix=[]
for datels in date:
       	file_prefix=time+'z'
        for fname in range(24,246,6):
        	fstr= str(fname)
 		if (len(fstr)<3):
			jstr='f'+'0'+fstr
		else:
			jstr='f'+fstr
		file_suffix.append(jstr)

        #file_suffix=['f006','f012','f018']
	#print(file_suffix)
        for suffix in file_suffix:
		filename='nwm.'+file_prefix+'.medium_range.terrain_rt.'+ suffix + '.conus.nc'
		KEY = model_name+'/'+ datels +'/'+ time + '/'+ 'nwm.'+ file_prefix+ '.medium_range.terrain_rt.'+ suffix + '.conus.nc' # replace with your object key
		s3 = boto3.resource('s3')
		path='/raidStorage/nwm_data/'+ model_name+'/'+datels +'/'+time
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
