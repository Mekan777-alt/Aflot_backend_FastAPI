from mongoengine import (Document, EmailField, IntField, StringField, DateTimeField, BooleanField, DateField,
                         EmbeddedDocument, EmbeddedDocumentField, ListField)
from mongoengine.fields import ObjectIdField


class Auth(Document):

    email = EmailField(unique=True)
    inn = IntField(unique=True)
    phone_number = StringField(unique=True)
    hashed_password = StringField()
    role = StringField()
    is_active = BooleanField()
    is_superuser = BooleanField()
    is_verified = BooleanField()
    last_login = DateTimeField()
    salt = StringField()


class Ship(Document):
    position = StringField()
    salary = StringField()
    date_of_departure = DateField()
    contract_duration = StringField()
    ship_name = StringField()
    imo = StringField()
    ship_type = StringField()
    year_built = IntField()
    contact_person = StringField()
    status = StringField()
    email = EmailField()
    dwt = IntField()
    kw = IntField()
    length = IntField()
    width = IntField()
    phone1 = StringField()
    phone2 = StringField()



class Position(EmbeddedDocument):
    position_name = StringField()


class Worked(EmbeddedDocument):
    worked = StringField()


class Vacancies(EmbeddedDocument):
    id = ObjectIdField


class BlackList(EmbeddedDocument):
    id = ObjectIdField


class Favorites(EmbeddedDocument):
    id = ObjectIdField


class UserModel(Document):

    email = EmailField(unique=True)
    phone_number = StringField()
    first_name = StringField()
    last_name = StringField()
    patronymic = StringField()
    role = StringField()
    country = StringField()
    region = StringField()
    city = StringField()
    telegram = StringField()
    positions = ListField(EmbeddedDocumentField(Position))
    worked = ListField(EmbeddedDocumentField(Worked))


class CompanyModel(Document):

    email = EmailField(unique=True)
    phone_number = StringField(unique=True)
    first_name = StringField()
    last_name = StringField()
    patronymic = StringField()
    role = StringField()
    telegram = StringField()
    company_name = StringField()
    company_inn = IntField(unique=True)
    company_address = StringField()
    favorites = ListField(EmbeddedDocumentField(Favorites))
    black_list = ListField(EmbeddedDocumentField(BlackList))
    vacancies = ListField(EmbeddedDocumentField(Vacancies))
