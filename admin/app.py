import datetime

from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette_admin.contrib.mongoengine import Admin, ModelView
from mongoengine import connect, disconnect
from mongoengine import (Document, EmailField, IntField, StringField, DateTimeField, BooleanField, DateField,
                         EmbeddedDocument, EmbeddedDocumentField, ListField, ImageField)
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


class Contact(Document):
    email = EmailField(unique=True)
    phone_number = StringField()
    whatsapp = StringField()
    inn = IntField(unique=True)
    legal_address = StringField()
    requisites = StringField()


class Position(Document):
    position_name = StringField()


class Vessel(Document):
    vessel_name = StringField()


class NewsModel(Document):
    title = StringField()
    content = StringField()
    created_at = DateField()
    photo_path = ImageField()
    view_count = IntField()


class RealHistory(Document):
    title = StringField()
    content = StringField()


app = Starlette(
    routes=[
        Route(
            "/",
            lambda r: HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>'),
        )
    ],
    on_startup=[lambda: connect(db="aflot_backend", host="localhost", port=27017)],
    on_shutdown=[lambda: disconnect()],
)

# Create admin
admin = Admin(title="Admin: MongoEngine")


# Add views
class UserView(ModelView):
    pass


admin.add_view(UserView(Auth, icon="fa fa-users"))
admin.add_view(UserView(CompanyModel, icon="fa fa-users"))
admin.add_view(ModelView(UserModel, icon="fa fa-users"))
admin.add_view(ModelView(Ship, icon="fa fa-users"))
admin.add_view(ModelView(NewsModel, icon="fa fa-blog"))
admin.add_view(ModelView(Contact, icon="fa fa-users"))
admin.add_view(ModelView(Vessel, icon="fa fa-users"))
admin.add_view(ModelView(Position, icon="fa fa-users"))
admin.add_view(ModelView(RealHistory, icon="fa fa-blog"))

admin.mount_to(app)
