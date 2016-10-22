import math
import json

from geopy.distance import great_circle
from geopy.geocoders import Nominatim

from .map_generator import generate_map_img
from .resources import load_100women_and_countries, Coords


def match(user):
    women100, countries = load_100women_and_countries()

    age_match = match_on_age(user, women100)
    location_match, map_file = match_on_location(user, women100)
    return format_response(user, location_match, age_match, map_file)


def match_on_age(user, women100):
    if not user or not user.age:
        return None

    women_with_age_set = [w for w in women100 if w.age is not None]
    delta_age_f = lambda woman: math.fabs(woman.age - user.age)
    age_sorted = sorted(women_with_age_set, key=delta_age_f)
    return age_sorted[0]


def match_on_location(user, women100):
    hometown_coords = get_hometown_coords(user.hometown)
    if not hometown_coords:
        return None

    closest_woman = find_woman_with_closest_location(hometown_coords, women100)
    map_file = generate_map_content((hometown_coords.lat, hometown_coords.lng),
                                    (closest_woman.country.coords.lat, closest_woman.country.coords.lng))
    return closest_woman, map_file


def generate_map_content(user_coords, woman_coords):
    if user_coords and woman_coords:
        map_filename = generate_map_img(user_coords, woman_coords)
        if map_filename is not None:
            return map_filename

    return None


def find_woman_with_closest_location(hometown_coords, women100):
    closest_woman = None
    closest_distance = None
    for woman in women100:
        if not woman.country:
            continue

        dist = earth_distance(hometown_coords, woman.country.coords)

        if closest_distance is None or dist < closest_distance:
            closest_woman = woman
            closest_distance = dist

    return closest_woman


def get_hometown_coords(hometown):
    geolocator = Nominatim()
    location = geolocator.geocode(hometown)
    if location:
        return Coords(lat=location.latitude, lng=location.longitude)


def earth_distance(coords1, coords2):
    return round(great_circle(coords1, coords2).meters, 2)


def format_response(user, location_match, age_match, map_file):
    result = {}
    result['user'] = user.__dict__ if user else {}

    match_result = {}
    if age_match:
        match_result['by_age'] = age_match.to_dict()
    if location_match:
        match_result['by_location'] = location_match.to_dict()

    result['matches'] = match_result
    if map_file:
        result['map_file'] = map_file
    return result

import unittest


class TestMatch(unittest.TestCase):

    def test_age_match(self):
        user = User(age=50)
        women100, _ = load_100women_and_countries()
        best_match = match_on_age(user, women100)
        self.assertEqual(49, best_match.age)
        self.assertEqual('Tina', best_match.firstname)

    def test_earth_dist(self):
        coords1 = Coords(51, 0)
        coords2 = Coords(51, 0.01)
        self.assertEqual(699.97, earth_distance(coords1, coords2))

    def test_loc_match(self):
        user = User(hometown='Dublin')
        women100, _ = load_100women_and_countries()
        _, best_match = match_on_location(user, women100)
        self.assertEqual('british', best_match.nationality)


if __name__ == '__main__':
    unittest.main()
