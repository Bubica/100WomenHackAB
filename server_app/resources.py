from collections import namedtuple
import csv
import os

WOMEN_FILENAME = '100women.csv'
COUNTRIES_COORDS_FILENAME = 'cow.csv'
COUNTRIES_NATIONALITIES_FILENAME = 'country_nationalities.csv'

Coords = namedtuple('Coords', 'lat,lng')


class User(object):

    def __init__(self, firstname=None, surname=None, profile_photo_url=None, hometown=None, age=None):
        self.firstname = firstname
        self.surname = surname
        self.profile_photo_url = profile_photo_url
        self.hometown = hometown
        self.age = age

    def __repr__(self):
        return "firstname: {}, surname: {}, age: {}, hometown: {}".format(self.firstname, self.surname, self.age, self.hometown)

    def __eq__(self, other):
        return self.age == other.age and self.hometown == other.hometown and \
            self.firstname == other.firstname and self.surname == other.surname


class Woman(object):

    def __init__(self, age, _id, firstname, surname, job, nationality, bio_paragraph1, bio_paragraph2,
                 bio_paragraph3, description, _filter, image, link_url, link_text, country=None):

        self.age = age
        self.id = _id
        self.firstname = firstname
        self.surname = surname
        self.job = job
        self.nationality = nationality
        self.bio_paragraph1 = bio_paragraph1
        self.bio_paragraph2 = bio_paragraph2
        self.bio_paragraph3 = bio_paragraph3
        self.description = description
        self.filter = _filter
        self.image = image
        self.link_url = link_url
        self.link_text = link_text
        self.country = country

    @classmethod
    def from_dict(cls, dct):
        return cls(
            age=int(dct.get('age')) if dct.get('age') else None,
            _id=dct.get('id'),
            firstname=dct.get('firstname'),
            surname=dct.get('surname'),
            job=dct.get('job'),
            nationality=dct.get('nationality').strip().lower(),
            bio_paragraph1=dct.get('bio_paragraph1'),
            bio_paragraph2=dct.get('bio_paragraph2'),
            bio_paragraph3=dct.get('bio_paragraph3'),
            description=dct.get('description'),
            _filter=dct.get('filter'),
            image=dct.get('image'),
            link_url=dct.get('link_url'),
            link_text=dct.get('link_text')
        )

    def to_dict(self):
        return {
            'age': self.age,
            'firstname': self.firstname,
            'surname': self.surname,
            'nationality': self.nationality,
        }

    def __repr__(self):
        return "firstname: {}, surname: {}, age: {}, nationality: {}".format(self.firstname, self.surname, self.age, self.nationality)


class Country(object):

    def __init__(self, name=None, capital=None, coords=None, nationality=None):
        self.name = str(name.strip().lower()) if name else None
        self.capital = str(capital.strip().lower()) if capital else None
        self.coords = coords
        self.nationality = str(nationality.strip().lower()) if nationality else None


def load_100women_and_countries():
    women = load_100women()
    countries = load_countries()

    for woman in women:
        country = get_country_of_origin(woman, countries)
        woman.country = country

    return women, countries


def load_100women():
    women = []
    filename = load_resource_filename(WOMEN_FILENAME)
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for record in reader:
            woman = Woman.from_dict(record)
            women.append(woman)

    return women


def load_countries():
    filename = load_resource_filename(COUNTRIES_COORDS_FILENAME)
    countries = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for record in reader:
            name = record.get('ISOen_name')
            coords = Coords(lat=float(record.get('latitude')), lng=float(record.get('longitude')))
            capital = record.get('BGN_capital')
            nationality = record.get('BGN_demomyn_adj').split(',')[-1]
            country = Country(name=name, coords=coords, capital=capital, nationality=nationality)
            countries.append(country)
    return countries


def _load_countries_and_nationalities():
    filename = load_resource_filename(COUNTRIES_NATIONALITIES_FILENAME)
    countries = {}
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for record in reader:
            name = record.get('en_short_name')
            nationality = record.get('nationality')
            country = Country(name=name, nationality=nationality)
            countries[country.name] = country
    return countries


def get_country_of_origin(woman, countries):
    for country in countries:
        if country.nationality == woman.nationality:
            return country
    return None


def load_resource_filename(resource_name):
    resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
    return os.path.join(resources_dir, resource_name)
