import xarray as xr
from pymapd import connect
import pyarrow as pa;import numpy as np
import pandas as pd
from pyproj import Proj, transform
conn=connect(user="mapd", password="i-0c8cb37b31ea60c5a", host="localhost", dbname="mapd")
import mzgeohash
import unicodedata
from datetime import datetime
filename='nwm-v1.2-channel_spatial_index.nc'
path='/raidStorage/nwm_data/'
file=path+'/'+filename
print(file)
ds = xr.open_dataset(file)
df = ds.to_dataframe()
df =  df.reset_index()
#print(df.head())
conn.load_table("channel_coordinates",df,create='infer',method='arrow')
