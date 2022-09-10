import bspice as bs
from datetime import datetime


obs_loc = (7.744083817548831, 48.58313582900411, 140)

adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
#adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030_earth_sun_moon.bsp']

t1 = datetime(2022, 9, 10)
t2 = datetime(2022, 9, 11)

r_az_alt = bs.get_apparent_window(10, t1, t2, 24, obs_loc, kernels, abcorr='LT+S')

for i in r_az_alt:
    print(f'Az:{i[1]} ||| Alt:{i[2]}')


