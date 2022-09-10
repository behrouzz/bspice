**Author:** [Behrouz Safari](https://astrodatascience.net/)<br/>
**License:** [MIT](https://opensource.org/licenses/MIT)<br/>

# bspice
*Working with SPICE kernels*


## Installation

You can install the latest version of *bspice* from [PyPI](https://pypi.org/project/bspice/):

    pip install bspice

The requirements are *numpy*, *requests* and *spiceypy*.


## Download Kernels

```python
import bspice as bs

bs.download_kernels(overwrite=False, solsys=True, jupiter=True)
```

## Apparent position of Saturn

```python
import bspice as bs
from datetime import datetime

t = datetime.utcnow()
obs_loc = (7.744083817548831, 48.58313582900411, 140)

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030.bsp']

r, az, alt = bs.get_apparent(6, t, obs_loc, kernels)
print(az, alt)
```

## Apparent position of Jupiter Moons

```python
import bspice as bs
from datetime import datetime
import matplotlib.pyplot as plt

t = datetime.utcnow()
obs_loc = (7.744083817548831, 48.58313582900411, 140)

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'jup4_2030.bsp']

bodies = [599, 501, 502, 503, 504]
r_az_alt = bs.get_apparent_bodies(bodies, t, obs_loc, kernels, abcorr='LT+S')
print(r_az_alt)

fig, ax = plt.subplots()
ax.scatter(r_az_alt[0,1], r_az_alt[0,2])
ax.scatter(r_az_alt[1:,1], r_az_alt[1:,2])
plt.show()
```

## Apparent position of the Sun during 24 hours

```python
import bspice as bs
from datetime import datetime

obs_loc = (7.744083817548831, 48.58313582900411, 140)

adr = 'C:/Moi/_py/Astronomy/Solar System/kernels/'

kernels = [adr+i for i in bs.main_kernels]
kernels = kernels + [adr+'de440_2030_earth_sun_moon.bsp']

t1 = datetime(2022, 9, 10)
t2 = datetime(2022, 9, 11)

r_az_alt = bs.get_apparent_window(10, t1, t2, 24, obs_loc, kernels, abcorr='LT+S')

for i in r_az_alt:
    print(f'Az:{i[1]} ||| Alt:{i[2]}')
```
