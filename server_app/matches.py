import math
import json

from .women100 import load_100women, load_countries

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


def match(user):
    women100, countries = load_100women_and_countries()

    user = User(hometown='Zagreb')
    location_match = match_on_location(user, women100)
    # age_match = match_on_location(user, women100)

    # return format_response(location_match, age_match)


def age_match(user, women100):
    if not user or not user.age:
        return None

    delta_age_f = lambda woman: math.fabs(woman.age - user.age)
    age_sorted = sorted(women100, key=delta_age_f)
    return age_sorted[0]


def location_match(user, women100):
    countries = load_countries()
    user_hometown_coords = get_hometown_coords(user.hometown, countries)
    if not user_hometown_coords:
        return None

    find_woman_with_closest_location


def get_hometown_coords(hometown, countries):
    for country in countries:
        if country.capital == hometown.strip().lower():
            return country
    return None
