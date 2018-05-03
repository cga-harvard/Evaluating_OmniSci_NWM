import xarray as xr
import gc
from pymapd import connect
import pyarrow as pa;import numpy as np
import pandas as pd
from pyproj import Proj, transform
conn=connect(user="mapd", password="i-0c8cb37b31ea60c5a", host="localhost", dbname="mapd")
import mzgeohash
import unicodedata
from datetime import datetime
model_name='analysis_assim'
date=['20180101','20180102','20180103','20180104','20180105','20180106','20180107','20180108','20180109','20180110']
time='t00'
#time=['t00']
for datels in date:
        file_prefix=time+'z'
        filename='nwm.'+file_prefix+'.analysis_assim.channel_rt.tm00.conus.nc'
        path='/raidStorage/nwm_data/'+ model_name+'/'+datels+'/'+time
        file=path+'/'+filename
        print(file)
        #if('24' in file):
        #   print(file)
	ds = xr.open_dataset(file)
	df = ds.to_dataframe()
        #print("df head is", df.head())
	df=df.reset_index()
        #print("df head is", df.head())
	df=df.drop(['reference_time', 'time','nudge'], axis=1)
        #print("df head is", df.head())
	#inProj = Proj('+proj=lcc +lat_1=30 +lat_2=60 +lat_0=40.0000076294 +lon_0=-97 +x_0=0 +y_0=0 +a=6370000 +b=6370000 +units=m +no_defs')
	#outProj = Proj('+init=epsg:4326')
	#x = df['x'].values
	#y = df['y'].values
	#geo_x,geo_y = transform(inProj,outProj,x,y)
	#df.loc[:,'geo_x'] = geo_x
        #df['geo_x']=geo_x
        #df['geo_y']=geo_y
	#df.loc[:,'geo_y'] = geo_y
	#df = df[ (df['geo_x']<=-93.51) & (df['geo_x']>=-106.65) & (df['geo_y']<=36.5) & (df['geo_y']>=25.84)]
	#df['id'] = pd.factorize(((df.geo_x).astype(str))+((df.geo_y).astype(str)))[0]
        #df=df.drop(['x', 'y', 'geo_x','geo_y'], axis=1)
        #df=df.drop([''], axis=1)
	phenomenon_time = (ds.attrs['model_output_valid_time']).replace('_'," ")
	phenomenon_time_str =  unicodedata.normalize('NFKD', phenomenon_time).encode('ascii','ignore')
	phenomenon_time_date =  datetime.strptime(phenomenon_time_str, '%Y-%m-%d %H:%M:%S')
	phenomenon_time_utc=  phenomenon_time_date.strftime('%Y-%m-%d %H:%M:%S')
	#df.loc[:,'phenomenon_time']= phenomenon_time_utc
	#df.loc[:,'valid_time']= phenomenon_time_utc
        df['phenomenon_time']=phenomenon_time_utc
        df['valid_time']=phenomenon_time_utc 
	df['phenomenon_time'] =  pd.to_datetime(df['phenomenon_time'])
	df['valid_time'] =  pd.to_datetime(df['valid_time'])
	#df.to_parquet('/raidStorage/nwm_data/nwm.t00z.analysis_assim.terrain_rt.tm00.conus.parquet')
	#print(df.head)
        #df=df.iloc[::5, :]
	conn.load_table("nwm_channel",df,create='infer',method='arrow')
        del(df)
        del(ds)
        gc.collect()
        #print(df.head)
