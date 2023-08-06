from astropy.io import fits
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
import twirl
from twirl.utils import *
import astropy.wcs.utils as wcsutils


filepath = "/Users/lionelgarcia/Data/Trappist-South_20201130_TOI-860.01_z/TRAPPS.2020-12-01T04_31_56.109_reduced.fits"

hdu = fits.open(filepath)
science = hdu[0]

header = science.header
data = science.data

# ra, dec in degrees
ra, dec = header["RA"], header["DEC"]
target = SkyCoord(ra, dec, unit=(u.deg, u.deg))

# image shape and pixel size in "
shape = data.shape
pixel = 0.66

stars = twirl.find_peaks(data)
radec = twirl.gaia_radec(target, shape, pixel)
_radec = SkyCoord(*radec.T, unit=(u.deg, u.deg))

M = twirl.utils.find_transform(radec, stars, show=True, tolerance=10)
s1, s2 = cross_match(stars, affine_transform(M)(radec))
pass
#header.update(wcs.to_header())
#hdu.writeto(filepath, overwrite=True)