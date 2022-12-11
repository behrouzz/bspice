import bspice as bs
from hypatie.transform import sph2car, angular_separation
import numpy as np


def sso_star(sso, ra, dec, plx, obs_loc, t):
    # sso
    sso_gcrs, vel_g, lt_g = bs.gcrs(sso, t, kernels, abccorr='NONE')
    az_sso, alt_sso, dist_sso = bs.gcrs_to_altaz(t, obs_loc, sso_gcrs, kernels)
    # star
    d_pc = 1 / (plx*1000)
    d_km = d_pc * 30856775814913.67
    star_icrs = sph2car(np.array([ra, dec, d_km]))
    star_gcrs = bs.icrs_to_gcrs(star_icrs, t, kernels, abccorr='NONE')
    az_star, alt_star, dist_star = bs.gcrs_to_altaz(t, obs_loc, star_gcrs, kernels)
    # separation
    ang_sep = angular_separation(az_sso, alt_sso, az_star, alt_star)
    return az_sso, alt_sso, az_star, alt_star, ang_sep



#adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
adr = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'

kernels = [adr + 'naif0012.tls',
           adr + 'pck00010.tpc',
           adr + 'earth_latest_high_prec.bpc',
           adr + 'de440s.bsp']


# inputs
obs_loc = (7.744083817548831, 48.58313582900411, 140)
t = '2022-12-08 05:00:00'

sso = 301
ra = 222.7196379
dec = -16.0417765
plx = 43.03


az_sso, alt_sso, az_star, alt_star, ang_sep = \
        sso_star(sso, ra, dec, plx, obs_loc, t)

print('SSO : ', az_sso, alt_sso)
print('Star: ', az_star, alt_star)
print('ang_sep: ', ang_sep)

#from hypatie.catalogues import Catalogue
#cat = Catalogue(name='hipparcos', where='Vmag < 3', n_max=1000)
#data, meta = cat.download()
