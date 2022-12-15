import json
import requests
import os
import pandas as pd
import folium

class earthquake_info:

    def __init__(self, f_start, f_end, f_location):
        self.f_start = f_start
        self.f_end = f_end
        self.f_location = f_location

    def get_earthquake_info(self):

        """
        The 'get_earthquake_info' is a python package that can query global earthquake information by date and location and visualize the information at the same time.

        Parameters
        ----------
        f_start : Starting date. Query the earthquake information starting from the initial time according to the input starting date. (string)
        f_end : Ending data. Query the earthquake information before the end time according to the input end date. (string)
        f_location : Country or region name. According to the input location, query the earthquake information that occurred near the location. (string)

        Returns
        -------
        The output is a table of earthquake information that occurred near the input location at the same time as the input date. Besides, the earthquake location is marked on the map, and the html file of the map is output for users to view the specific location of the earthquake.


        Examples
        --------
        >>> from earthquake_information_wd2366 import earthquake_information_wd2366
        >>> get_info = earthquake_information_wd2366.earthquake_info('2022-12-13','2022-12-14', ['Hawaii', 'Washington'])
        >>> get_info.get_earthquake_info()
                 Date      Time Magnitude  ...  Depth  Longitude    Latitude
        0  2022-12-14  21:45:38       3.3  ...  33.59  19.208333 -155.372500
        1  2022-12-14  20:56:46       2.9  ...  12.68  46.624167 -121.756333
        2  2022-12-14  18:47:23       2.9  ...   5.95  20.449833 -155.664993
        3  2022-12-14  11:32:01       2.5  ...  30.79  19.189501 -155.393005
        4  2022-12-14  04:05:41       2.6  ...   1.06  19.424500 -155.254166

        And a map file called "earthquake_info.html" is downloaded to the same local path.
       """

        response = requests.get("https://api.weatherusa.net/v1/earthquake")
        earthquake = response.json()
        data = earthquake['data']['features']

        date = []
        time = []
        update_time = []
        magnitude = []
        place = []
        felt_count = []
        status = []
        type_0 = []
        cdi = []
        mmi = []
        sig = []
        depth = []
        longitude = []
        latitude = []

        for i in range(0, len(data)):
            date.append(data[i]['properties']['time'][0:10])
            time.append(data[i]['properties']['time'][11:19])
            magnitude.append(data[i]['properties']['magnitude'])
            place.append(data[i]['properties']['place'])
            felt_count.append(data[i]['properties']['felt_count'])
            status.append(data[i]['properties']['status'])
            cdi.append(data[i]['properties']['cdi'])
            mmi.append(data[i]['properties']['mmi'])
            sig.append(data[i]['properties']['sig'])
            depth.append(data[i]['properties']['depth'])
            longitude.append(data[i]['geometry']['coordinates'][1])
            latitude.append(data[i]['geometry']['coordinates'][0])

        date = pd.DataFrame(date, columns=['Date'])
        time = pd.DataFrame(time, columns=['Time'])
        magnitude = pd.DataFrame(magnitude, columns=['Magnitude'])
        place = pd.DataFrame(place, columns=['Place'])
        felt_count = pd.DataFrame(felt_count, columns=['Felt_count'])
        status = pd.DataFrame(status, columns=['Status'])
        cdi = pd.DataFrame(cdi, columns=['CDI'])
        mmi = pd.DataFrame(mmi, columns=['MMI'])
        sig = pd.DataFrame(sig, columns=['SIG'])
        depth = pd.DataFrame(depth, columns=['Depth'])
        longitude = pd.DataFrame(longitude, columns=['Longitude'])
        latitude = pd.DataFrame(latitude, columns=['Latitude'])

        join0 = date.join(time)
        join1 = join0.join(magnitude)
        join2 = join1.join(place)
        join3 = join2.join(felt_count)
        join4 = join3.join(status)
        join5 = join4.join(cdi)
        join6 = join5.join(mmi)
        join7 = join6.join(sig)
        join8 = join7.join(depth)
        join9 = join8.join(longitude)
        final = join9.join(latitude)

        final_date = final.loc[(final['Date'] >= self.f_start) & (final['Date'] <= self.f_end), :]
        Place = self.f_location
        Location = '|'.join(Place)
        final_place = final_date[final_date['Place'].str.contains(Location)]
        final_place = final_place.reset_index(drop=True)

        earthquake_map = folium.Map(location=[final_place['Longitude'][0], final_place['Latitude'][0]], zoom_start=12, tiles="Stamen Terrain")
        for i in range(len(final_place)):
            folium.Marker(
                location=[final_place['Longitude'][i], final_place['Latitude'][i]],
                popup=final_place['Place'][i],
                icon=folium.Icon(color='red')
            ).add_to(earthquake_map)

        earthquake_map.save("earthquake_info.html")
        print(final_place)
        return final_place
