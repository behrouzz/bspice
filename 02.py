import bspice as bs
from datetime import datetime

t = datetime.utcnow()
obs_loc = (7.744083817548831, 48.58313582900411, 140)

#adr = 'https://raw.githubusercontent.com/behrouzz/astrodata/main/spice/kernels/'
#adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2022_2025.bsp', adr+'jup380s_2225.bsp']


r, az, alt = bs.get_apparent(301, t, obs_loc, kernels)
print(az, alt)
