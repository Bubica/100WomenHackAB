import os
import time

import folium
from folium import plugins

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def generate_map(user_coords, woman_coords, path='world.html'):
    location = get_center_coords(user_coords, woman_coords)
    folium_map = folium.Map(location=location, zoom_start=4, tiles='Stamen Terrain')

    folium.Marker(user_coords, popup="User", icon=folium.Icon(icon='cloud')).add_to(folium_map)
    folium.Marker(woman_coords, popup="Your best match", icon=folium.Icon(color='green')).add_to(folium_map)

    folium_map.save(path)


def get_center_coords(c1, c2):
    return (c1[0] + c2[0]) / 2., (c1[1] + c2[1]) / 2.


def generate_map_img(user_coords, woman_coords, path=None):
    try:
        # REQUIRES: export PATH=$PATH:/Users/agata/Downloads
        filename = path or 'world.html'
        generate_map(user_coords, woman_coords, path=filename)

        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        browser = webdriver.Firefox(capabilities=firefox_capabilities)

        tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=filename)
        browser.get(tmpurl)
        time.sleep(1)
        browser.save_screenshot('world.png')
        browser.quit()
    except:
        return False

    return True

if __name__ == '__main__':
    generate_map_img((51, 0), (33, 0))
