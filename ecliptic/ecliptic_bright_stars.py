import numpy as np
import pandas as pd
from hypatie.transform import equ_sph2ecl_sph, sph2car, car2sph
from bspice import earth_icrs


def equ2ecl(pos_equ_sph):
    # both sph
    pos_equ_car = sph2car(pos_equ_sph)

    e = (23 + 26/60 + 21.448/3600) * (np.pi/180)
    arr = np.array([[1,  0,         0        ],
                    [0,  np.cos(e), np.sin(e)],
                    [0, -np.sin(e), np.cos(e)]])
    pos_ecl_car = np.matmul(arr, pos_equ_car)
    
    pos_ecl_sph = car2sph(pos_ecl_car)
    return pos_ecl_sph
    




df = pd.read_csv('hip3.csv')

#equ_sph2ecl_sph

ra , dec = 2.096911, 29.090432

a = np.array([ra, dec, 1])

#df['radec'] = df[['_RA_icrs']].apply(lambda x: x['_RA_icrs'])

ra_dec_r = []
for i, row in df.iterrows():
    r = (1 / (row['Plx']*1000)) * 30856775814913.67
    ra_dec_r.append(np.array([row['_RA_icrs'], row['_DE_icrs'], r]))
    

ecliptics = [equ2ecl(i) for i in ra_dec_r]

df['ecl_lat'] = [i[1] for i in ecliptics]
df['abs_ecl_lat'] = abs(df['ecl_lat'])
df = df.sort_values(by='abs_ecl_lat')
df = df[df['abs_ecl_lat']<10]
del df['abs_ecl_lat']

