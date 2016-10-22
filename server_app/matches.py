import math
import json

from geopy.geocoders import Nominatim

from .resources import load_100women_and_countries

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


class User(object):
    __slots__ = ('name', 'profile_photo_url', 'hometown', 'age')

    def __init__(self, name=None, profile_photo_url=None, hometown=None, age=None):
        self.name = name
        self.profile_photo_url = profile_photo_url
        self.hometown = hometown
        self.age = age


def match(user):
    women100, countries = load_100women_and_countries()

    user = User(hometown='Zagreb')
    location_match = match_on_location(user, women100)
    # age_match = match_on_location(user, women100)

    # return format_response(location_match, age_match)


def age_match(user, women100):
    if not user or not user.age:
        return None

    women_with_age_set = [w for w in women100 if w.age is not None]
    delta_age_f = lambda woman: math.fabs(woman.age - user.age)
    age_sorted = sorted(women_with_age_set, key=delta_age_f)
    return age_sorted[0]


def location_match(user, women100):
    countries = load_countries()
    hometown_coords = get_hometown_coords(user.hometown, countries)
    if not user_hometown_coords:
        return None

    find_woman_with_closest_location()


def get_hometown_coords(hometown, countries):
    geolocator = Nominatim()
    location = geolocator.geocode(hometown)
    if location:
        return (location.latitude, location.longitude)


import unittest


class TestMatch(unittest.TestCase):

    def test_age_match(self):
        user = User(age=50)
        women100, _ = load_100women_and_countries()
        best_match = age_match(user, women100)
        self.assertEqual(49, best_match.age)
        self.assertEqual('Tina', best_match.firstname)


if __name__ == '__main__':
    unittest.main()
