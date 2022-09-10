import bspice as bs
from datetime import datetime
import matplotlib.pyplot as plt

t = datetime.utcnow()
obs_loc = (7.744083817548831, 48.58313582900411, 140)

adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
#adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'jup4_2030.bsp']


bodies = [599, 501, 502, 503, 504]
r_az_alt = bs.get_apparent_bodies(bodies, t, obs_loc, kernels, abcorr='LT+S')
print(r_az_alt)

fig, ax = plt.subplots()
ax.scatter(r_az_alt[0,1], r_az_alt[0,2])
ax.scatter(r_az_alt[1:,1], r_az_alt[1:,2])
plt.show()
