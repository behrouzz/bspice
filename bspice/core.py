import spiceypy as sp
import requests, os
from glob import glob
import numpy as np

NAIF = 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/'

d2r = 3.141592653589793/180
r2d = 180/3.141592653589793

path = 'bs_kernels/'

dc_kernels = {
    'naif0012.tls': 'lsk/naif0012.tls',
    'pck00010.tpc': 'pck/pck00010.tpc',
    'earth_latest_high_prec.bpc': 'pck/earth_latest_high_prec.bpc',
    #'earth_200101_990628_predict.bpc': 'pck/earth_200101_990628_predict.bpc',
    }

main_kernels = list(dc_kernels.keys())

def download_kernels(overwrite=False, solsys=True, jupiter=False):
    if not os.path.isdir(path):
        os.mkdir(path)
    old_files = glob(path + '/*')
    old_filenames = [i.split('\\')[-1] for i in old_files]

    if solsys:
        dc_kernels['de440s.bsp'] = 'spk/planets/de440s.bsp'
    if jupiter:
        dc_kernels['jup329.bsp'] = 'spk/satellites/a_old_versions/jup329.bsp'

    if overwrite:
        for k,v in dc_kernels.items():
            download_file(NAIF+v, path=path)
            print(k, 'downloaded.')
    else:
        for k,v in dc_kernels.items():
            if k in old_filenames:
                print(k, 'already exists.')
            else:
                download_file(NAIF+v, path=path)
                print(k, 'downloaded.')
                



def download_file(url, path=''):
    filename = url.rsplit('/', 1)[-1]
    r = requests.get(url, allow_redirects=True)
    open(path+filename, 'wb').write(r.content)
    

def lonlat_to_cartesian(obs_loc):
    """
    obs_loc : (lon (deg), lat (deg), alt (m))
    """
    lon, lat, alt = obs_loc
    lon = lon * d2r
    lat = lat * d2r
    alt = alt / 1000
    radii = [6378.1366, 6378.1366, 6356.7519]
    re = radii[0]
    rp = radii[2]
    f = (re-rp)/re
    obspos = sp.pgrrec(body='earth', lon=lon, lat=lat, alt=alt, re=re, f=f)
    return obspos


##def get_icrs(body, t, kernels):
##    for k in kernels:
##        sp.furnsh(k)
##    et = sp.str2et(str(t))
##    state, lt = sp.spkez(targ=body, et=et, ref='J2000', abcorr='NONE', obs=0)
##    pos = state[:3]
##    vel = state[3:]
##    sp.kclear()
##    return pos, vel, lt


##def get_topocentric(body, t, obs_loc, kernels):
##    r,az,alt = get_apparent(body, t, obs_loc, kernels, abcorr='NONE')
##    for k in kernels:
##        sp.furnsh(k)
##    topo = sp.azlrec(range=r, az=az*d2r, el=alt*d2r,
##                     azccw=False, elplsz=True)
##    sp.kclear()
##    return topo


def get_apparent(body, t, obs_loc, kernels, abcorr='LT+S'):

    if isinstance(body, int):
        body = str(body)

    for k in kernels:
        sp.furnsh(k)

    et = sp.str2et(str(t))
    
    state, lt  = sp.azlcpo(
        method='ELLIPSOID',
        target=body,
        et=et,
        abcorr=abcorr,
        azccw=False,
        elplsz=True,
        obspos=lonlat_to_cartesian(obs_loc),
        obsctr='earth',
        obsref='ITRF93')

    r, az, alt = state[:3]

    sp.kclear()

    return r, az*r2d, alt*r2d


def gcrs_to_altaz(t, obs_loc, pos_gcrs, kernels=None):
    # Calculate ecef2enu rotation matrix
    lon, lat, _ = obs_loc
    lon = lon * d2r
    lat = lat * d2r
    r1 = [-np.sin(lon), np.cos(lon), 0]
    r2 = [-np.cos(lon)*np.sin(lat), -np.sin(lon)*np.sin(lat), np.cos(lat)]
    r3 = [np.cos(lon)*np.cos(lat), np.sin(lon)*np.cos(lat), np.sin(lat)]
    ecef2enu_rot = np.array([r1, r2, r3])

    # Calculate J2000 to body-equator-and-prime-meridian rotation matrix
    for k in kernels:
        sp.furnsh(k)
    et = sp.str2et(str(t))
    j2000_to_earthfixed_rot = sp.tisbod(ref='J2000', body=399, et=et)[:3,:3]
    sp.kclear()

    # Calculate itrf, enu, altaz
    pos_itrf = np.matmul(j2000_to_earthfixed_rot, pos_gcrs)
    e, n, u = np.matmul(ecef2enu_rot, pos_itrf)
    r = np.hypot(e, n)
    rng = np.hypot(r, u)
    el = np.arctan2(u, r)
    az = np.mod(np.arctan2(e, n), 2*np.pi)    
    return az*r2d, el*r2d, rng


def get_crs(body, t, abcorr, obs, kernels):
    for k in kernels:
        sp.furnsh(k)
    et = sp.str2et(str(t))
    state, lt = sp.spkez(targ=body, et=et, ref='J2000', abcorr=abcorr, obs=obs)
    sp.kclear()
    pos = state[:3]
    vel = state[3:]
    return pos, vel, lt


def icrs(body, t, kernels, abccorr='NONE'):
    pos, _, _ = get_crs(body=body, t=t, abcorr=abccorr, obs=0, kernels=kernels)
    return pos


def gcrs(body, t, kernels, abccorr='NONE'):
    pos, _, _ = get_crs(body=body, t=t, abcorr=abccorr, obs=399, kernels=kernels)
    return pos


def earth_icrs(t, kernels, abccorr='NONE'):
    pos, _, _ = get_crs(body=399, t=t, abcorr=abccorr, obs=0, kernels=kernels)
    return pos

def icrs_to_gcrs(pos_icrs, t, kernels, abccorr='NONE'):
    earth = earth_icrs(t, kernels, abccorr)
    return pos_icrs - earth

def gcrs_to_icrs(pos_gcrs, t, kernels, abccorr='NONE'):
    earth = earth_icrs(t, kernels, abccorr)
    return pos_gcrs + earth

