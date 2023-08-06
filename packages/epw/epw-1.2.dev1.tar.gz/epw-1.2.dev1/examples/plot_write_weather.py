#!/usr/bin/env python3

import epw
import os
import numpy as np
import matplotlib.pyplot as plt
import tempfile

weather_obj = epw.weather.Weather()
weather_obj.read(file_path=epw.data.weather_san_francisco_tmy_path())

weather_obj.dataframe['Dry Bulb Temperature'] = np.sin(2. * np.pi / 24. * weather_obj.dataframe.index) * 10. + 12.

# WRITE THE MODIFIED WEATHER FILE ###########################################

home_path = epw.core.expand_path("~")

with tempfile.TemporaryDirectory(dir=home_path, prefix=".", suffix="_test") as temp_dir_path:
    dst_epw_path = os.path.join(temp_dir_path, "weather.epw")

    weather_obj.write(dst_epw_path)

    print("Write", dst_epw_path)

    df = epw.core.run_eplus(epw.data.idf_cube_path(),
                            weather_file_path=dst_epw_path)    # TODO

    df['DistrictHeating:Facility [J](Hourly)'].plot(figsize=(20, 8))
    plt.show()