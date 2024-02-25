#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 14:18:08 2024

This script extracts/modifies the elevation (HGT_M) variable
from a WRF Preprocessing System generated netCDF file.

@author: jrevier
"""

import shutil
import netCDF4 as nc
import scipy.ndimage
import numpy as np

#set paths
file = 'PATH_TO_ORIGINAL_netCDF_FILE'
newfile = 'PATH_TO_EDITED_netCDF_FILE'

#create a copy as a precaution
shutil.copy2(file, newfile)

#read in dataset
ds = nc.Dataset(file, 'r+')

#define the bounds of the edited area
x1 = 365
x2 = 425
y1 = 325
y2 = 415


#assign the heights of the edit domain
hgt = ds.variables['HGT_M'][0, y1:y2, x1:x2]

#use numpy mean as an initial smooth
#replace height values in the netcdf file
hgt[:,:] = np.mean(hgt)-150
ds.variables['HGT_M'][:, y1:y2, x1:x2] = hgt[:,:]

#extend and reassign the edit domain for second pass with Gaussian filter
x1 -= 5
x2 += 30
y1 -= 10
y2 += 10
hgt = ds.variables['HGT_M'][0, y1:y2, x1:x2]


# Apply Gaussian filter in 2 directions
hgt_filtered = scipy.ndimage.gaussian_filter1d(hgt, sigma =25, axis=0)
hgt_filtered2 = scipy.ndimage.gaussian_filter1d(hgt_filtered, sigma=10, axis=-1)

#replace the height values in the netCDF file
ds.variables['HGT_M'][:, y1:y2, x1:x2] = hgt_filtered2[:,:]


ds.close()
