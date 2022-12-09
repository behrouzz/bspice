import bspice as bs
from hypatie.coordinates import RAhms, DECdms
from hypatie.transform import sph2car
import numpy as np

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr + 'naif0012.tls',
           adr + 'pck00010.tpc',
           adr + 'earth_latest_high_prec.bpc',
           adr + 'de440s.bsp']

obs_loc = (7.744083817548831, 48.58313582900411, 140)
t = '2022-12-08 05:00:00'


# Moon
# ----
body = 301

moon_gcrs, vel_g, lt_g = bs.gcrs(body, t, kernels, abccorr='NONE')
az_moon, alt_moon, dist_moon = bs.gcrs_to_altaz(t, obs_loc, moon_gcrs, kernels)
print('Moon: ', az_moon, alt_moon)

# Star
# ----
# * alf02 Lib
# 14 50 52.71309 -16 02 30.3955

ra = RAhms(14, 50, 52.71309).deg
dec = DECdms('-', 16, 2, 30.3955).deg
plx = 43.03

d_pc = 1 / (plx*1000)
d_km = d_pc * 30856775814913.67

star_icrs = sph2car(np.array([ra, dec, d_km]))
star_gcrs = bs.icrs_to_gcrs(star_icrs, t, kernels, abccorr='NONE')
az_star, alt_star, dist_star = bs.gcrs_to_altaz(t, obs_loc, star_gcrs, kernels)
print('Star: ', az_star, alt_star)
