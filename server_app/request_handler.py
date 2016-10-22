from datetime import datetime
import math
import json

from .resources import User
from .matches import match
import unittest


def process_request(request_payload):
    user = parse_user(request_payload)
    if user:
        matches = match(user)
    return format_output(user, matches)


def format_output(user, matches):
    result = {}
    result['matches'] = matches or {}
    result['user'] = user.__dict__ if user else {}
    return json.dumps(result)


def parse_user(user_json_string):
    user_dict = json.loads(user_json_string)
    age = get_age_from_birthday(user_dict.get('birthday'))
    return User(
        firstname=user_dict.get('first_name'),
        surname=user_dict.get('last_name'),
        hometown=user_dict.get('hometown', {}).get('name'),
        age=age)


def get_age_from_birthday(born_string):
    date_today = datetime.now().date()
    born = parse_birthday_string(born_string)

    if not born:
        return None

    this_years_birthday = born.replace(year=date_today.year)
    if this_years_birthday <= date_today:
        return date_today.year - born.year
    else:
        return date_today.year - born.year - 1


def parse_birthday_string(birthday_string):
    if not birthday_string:
        return None

    birthday = None
    try:
        birthday = datetime.strptime(birthday_string, "%m/%d/%Y").date()
    except ValueError:
        pass
    return birthday


class TestMatch(unittest.TestCase):

    user_fixture = """
        {
          "birthday": "04/16/1983",
          "hometown": {
            "id": "116619061681465",
            "name": "Zagreb, Croatia"
          },
          "first_name": "Agata",
          "last_name": "Brajdic",
          "id": "10154711934932119"
        }
    """

    def test_age(self):
        self.assertEqual(33, get_age_from_birthday("04/16/1983"))
        self.assertEqual(32, get_age_from_birthday("12/16/1983"))

    def test_parse_user(self):
        user = parse_user(self.user_fixture)
        expected_user = User(age=33, firstname="Agata", surname="Brajdic", hometown="Zagreb, Croatia")
        self.assertEqual(expected_user, user)

    def test_process_request(self):
        match_dict_str = process_request(self.user_fixture)

        expected_dict = {
            'user': {'age': 33,
                     'firstname': 'Agata',
                     'hometown': 'Zagreb, Croatia',
                     'profile_photo_url': None,
                     'surname': 'Brajdic'
                     },
            'matches': {
                'by_age': {
                    'age': 33,
                    'firstname': 'Aissa ',
                    'nationality': 'french',
                    'surname': 'Edon'
                },
                'by_location': {
                    'age': 27,
                    'firstname': 'Zuzanna',
                    'nationality': 'polish',
                    'surname': 'Stanska'}
            }
        }
        self.assertDictEqual(expected_dict, json.loads(match_dict_str))

if __name__ == '__main__':
    unittest.main()
