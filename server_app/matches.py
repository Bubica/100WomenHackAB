import math
import json

from geopy.distance import great_circle
from geopy.geocoders import Nominatim

from .resources import load_100women_and_countries, Coords

# {
#     "user": {
#         "photo_url": "www.blah"

#     },
#     "matches": [
#         "nationality": 12,
#         "age":187
#     ],

#     "100women": [
#         {
#             "id": 1,
#             "name": "Hillary",
#             "photo": "www...",
#             "age":13
#         }
#     ]
# }


def match(user):
    women100, countries = load_100women_and_countries()

    age_match = match_on_age(user, women100)
    location_match = match_on_location(user, women100)

    return format_response(location_match, age_match)


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

    return find_woman_with_closest_location(hometown_coords, women100)


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


def format_response(location_match, age_match):
    result = {}
    if age_match:
        result['age'] = age_match.to_dict()
    if location_match:
        result['location'] = location_match.to_dict()
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
        best_match = match_on_location(user, women100)
        self.assertEqual('british', best_match.nationality)


if __name__ == '__main__':
    unittest.main()
