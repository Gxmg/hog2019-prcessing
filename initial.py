# -*- coding: ascii -*-
"""
<<DESCRIPTION OF SCRIPT>>
"""
from netCDF4 import Dataset
from csv import writer
from datetime import date
from os.path import exists
import math
from collections import defaultdict
import matplotlib.pyplot as plt
__author__ = 'Gerard Noseworthy gnoseworthy@gmail.com'
__maintainer__ = '$'
__vcs_id__ = '$'





# gdal_translate "path/to/raster.tif" -b 1 "path/to/result.tif"

# ds = Dataset(dataset)

sun_hours = [3.15, 3.84, 4.49, 5.52, 5.87, 5.21, 5.03, 4.71, 5.03, 4.71, 3.45,
             2.93]

# START = date(year=2015, month=1, day=1)

def add_one_month(orig_date):
    # advance year and month by one month
    new_year = orig_date.year
    new_month = orig_date.month + 1
    # note: in datetime.date, months go from 1 to 12
    if new_month > 12:
        new_year += 1
        new_month -= 12

    new_day = orig_date.day
    # while day is out of range for month, reduce by one
    while True:
        try:
            new_date = date(new_year, new_month, new_day)
        except ValueError as e:
            new_day -= 1
        else:
            break

    return new_date



def process_dataset(ds,param, solar_collection=None):
    """

    """
    start = date(year=2015, month=1, day=1)

    pot_result = defaultdict(float)
    var_result = defaultdict(float)


    lyr = ds.variables.get(param)
    top_pt = 48, -56
    bottom = 45 -48

    lat = ds.variables.get('lat')
    lon = ds.variables.get('lon')

    target_lat = [(int(i), l) for i,l in enumerate(lat) if 40 < l < 55]
    target_lon = [(int(i), l) for i,l in enumerate(lon) if 360-45 > l > 360-60]


    t_val = start
    for i, time in enumerate(lyr):
        dataset = t_val.month

        for xi, x in target_lat:
            for yi, y in target_lon:
                cld_pct = float(time[xi,yi])
                if solar_collection:
                    temp = solar_collection.get((t_val.year, float(x), float(y-360)))/12

                    pot_result[(t_val.year, float(x), float(y-360))] += wind_pot(cld_pct, temp)
                var_result[(t_val.year, float(x), float(y-360))] += cld_pct

        t_val = add_one_month(t_val)
    if solar_collection:
        out_data = r"C:\PROJECT\climate\monthly_wind_pot_all.csv"
        if exists(out_data):
            mode = 'a'
        else:
            mode = 'w'
        with open(out_data, 'w') as csv_out:
            csv_writer = writer(csv_out)
            csv_writer.writerow(('time', 'lat', 'lon', 'mean_temp', 'mean_wind', 'wind_potential'))

            for (t, x, y), pot in sorted(pot_result.items()):
                var = var_result.get((t, x, y))
                var2 = solar_collection.get((t,x,y)) - 273.15
                csv_writer.writerow((t, x, y, round(273.15- float(var2/12),2), round(var/12, 1), int(pot)))
    return var_result











def solar_pot(mth, cld_pct):
    """
    Calculate Solar Potential
    """
    return 0.75 * 254 * sun_hours[int(mth)-1] * (100-cld_pct)/100
# End solar_pot function


def wind_pot(surface_speed, temp):
    """

    """
    p = 101/(287.058 * (temp))
    ar = 11310

    pd = 0.5 * p * (surface_speed**3)

    return ar * pd * .32


# End wind_pot function


# End process_dataset function



if __name__ == '__main__':
    dataset = r"C:\Users\gnose\Downloads\tasmax_Amon_MRI-ESM2-0_ssp119_r1i1p1f1_gn_201501-210012.nc"
    ds = Dataset(dataset)
    col = process_dataset(ds, 'tasmax')
    dataset = r"C:\Users\gnose\Downloads\sfcWind_Amon_MRI-ESM2-0_ssp370_r1i1p1f1_gn_201501-210012.nc"
    ds = Dataset(dataset)
    process_dataset(ds, 'sfcWind', col)
    # print(wind_pot(6.07, 10))
