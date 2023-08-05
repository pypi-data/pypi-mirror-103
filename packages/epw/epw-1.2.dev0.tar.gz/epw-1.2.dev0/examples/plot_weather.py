#!/usr/bin/env python3

import epw
import matplotlib.pyplot as plt

weather_obj = epw.weather.Weather()
weather_obj.read(file_path=epw.data.weather_san_francisco_tmy_path())

df = weather_obj.dataframe
print(df.columns)

df.plot(y=['Dry Bulb Temperature', 'Dew Point Temperature'], figsize=(20, 8))
plt.show()