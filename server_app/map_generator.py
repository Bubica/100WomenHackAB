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
    folium_map.line(locations=[user_coords, woman_coords])

    folium_map.save(path)


def get_center_coords(c1, c2):
    return (c1[0] + c2[0]) / 2., (c1[1] + c2[1]) / 2.


def generate_map_img(user_coords, woman_coords, filename_stub=None):
    filename_png = None

    try:
        filename_html = '{}.html'.format(filename_stub or 'world')
        filename_png = '{}.png'.format(filename_stub or 'world')

        generate_map(user_coords, woman_coords, path=filename_html)

        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        browser = webdriver.Firefox(capabilities=firefox_capabilities)

        tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=filename_html)
        browser.get(tmpurl)
        time.sleep(1)
        browser.save_screenshot(filename_png)
        browser.quit()

    except:
        return None

    return filename_png

if __name__ == '__main__':
    generate_map_img((51, 0), (33, 0))
