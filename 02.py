import bspice as bs
from datetime import datetime
from glob import glob

t = datetime.utcnow()
obs_loc = (7.744083817548831, 48.58313582900411, 140)

kernels = glob('C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/*')

r, az, alt = bs.get_apparent(10, t, obs_loc, kernels)
print(az, alt)
