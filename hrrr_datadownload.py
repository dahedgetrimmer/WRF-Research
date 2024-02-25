# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script used to download archived HRRR Model (prs) GRIB2 files
using the Herbie Python Library.
"""


import herbie 
from herbie import Herbie


cwd = '/home/jrevier/HRRR_Data/' #where do you want the files to go

# lists of the model output hours and days wanted
days = ['06','07']
hours = ['00z', '03z', '06z', '09z', '12z', '15z', '18z', '21z']


#initialize the string you will use to cycle through days/hours 
dates = '2016-01-{}-{}'


# This loop uses the dates string defined above to loop through each day and
# the hours wanted for that day. Each iteration of the loop is used to create the 
# "date" argument in the Herbie function that searches for the connection to
# the GRIB2 file from the desired data base. 

for day in days:
    for hour in hours:
        
        if day == days[1] and hour == hours[-2]:  #I only needed up to 15z on the 7th
            break
        
        H = Herbie(date = dates.format(day, hour),      #defines the date of the output
                   model='hrrr',                        #defines the model 
                   product= 'prs',                      #defines the analysis of the model
                   fxx=00,                              #defines the forecast lead time
                   priority='aws')                      #defines the database to search
        
        H.download(save_dir=cwd)                        #downloads the found GRIB2 file to the directory stated above
        