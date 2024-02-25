#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 14:18:08 2024

@author: jrevier
"""

import shutil
import netCDF4 as nc
import scipy.ndimage
import numpy as np

file = '/home/jrevier/WRF/WPS/geo_em.d01.nc'
newfile = '/home/jrevier/WRF/WPS/og_met_em/geo_em_copy.nc'

shutil.copy2(file, newfile)

ds = nc.Dataset(file, 'r+')


x1 = 365
x2 = 425
y1 = 325
y2 = 415



hgt = ds.variables['HGT_M'][0, y1:y2, x1:x2]

hgt[:,:] = np.mean(hgt)-150
ds.variables['HGT_M'][:, y1:y2, x1:x2] = hgt[:,:]

x1 -= 5
x2 += 30
y1 -= 10
y2 += 10
hgt = ds.variables['HGT_M'][0, y1:y2, x1:x2]
sub_slope = ds.variables['VAR_SSO'][0, y1:y2, x1:x2]

sub_slope[:,:] = np.zeros( np.shape(sub_slope) )

# Apply Gaussian filter
hgt_filtered = scipy.ndimage.gaussian_filter1d(hgt, sigma =25, axis=0)
hgt_filtered2 = scipy.ndimage.gaussian_filter1d(hgt_filtered, sigma=10, axis=-1)

ds.variables['HGT_M'][:, y1:y2, x1:x2] = hgt_filtered2[:,:]
ds.variables['VAR_SSO'][: , y1:y2, x1:x2] = sub_slope[:, :]




#print(hgt_filtered)

ds.close()
