import datetime

from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette_admin.contrib.mongoengine import Admin, ModelView
from mongoengine import connect, disconnect
from mongoengine import (Document, EmailField, IntField, StringField, DateTimeField, BooleanField, DateField,
                         EmbeddedDocument, EmbeddedDocumentField, ListField, ImageField, FloatField)
from mongoengine.fields import ObjectIdField
from dotenv import load_dotenv
import os


class Auth(Document):
    resumeID = ObjectIdField()
    email = EmailField(unique=True)
    inn = IntField()
    phone_number = StringField(unique=True)
    hashed_password = StringField()
    role = StringField()
    is_active = BooleanField()
    is_superuser = BooleanField()
    is_verified = BooleanField()
    last_login = DateTimeField()
    date_joined = DateTimeField()
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
    id = ObjectIdField()


class BlackList(EmbeddedDocument):
    id = ObjectIdField()


class Favorites(EmbeddedDocument):
    id = ObjectIdField()


class FavoritesCompany(EmbeddedDocument):
    id = ObjectIdField()


class FavoritesVacancies(EmbeddedDocument):
    id = ObjectIdField()


class NotificationSettings(EmbeddedDocument):
    send_email = BooleanField()
    send_sms = BooleanField()
    send_telegram = BooleanField()
    mailing_notification = BooleanField()


class MainDocumentsUsers(EmbeddedDocument):
    foreign_passport = DateField()
    seafarers_ID_card = DateField()
    diploma = DateField()
    initial_safety_training = DateField()
    designated_safeguarding_responsibilities = DateField()
    dinghy_and_raft_specialist = DateField()
    fighting_fire_with_an_expanded_program = DateField()
    providing_first_aid = DateField()
    prevention_of_marine_pollution = DateField()
    tanker_certificate = DateField()
    occupational_health_and_safety = DateField()
    medical_commission = DateField()


class ShipwrightsPapers(EmbeddedDocument):
    gmssb = DateField()
    eknis = DateField()
    rlt = DateField()
    sarp = DateField()


class AdditionalDocuments(EmbeddedDocument):
    isolation_breathing_apparatus = DateField()
    naval_training = DateField()
    transportation_safety = DateField()
    tanker_certificate = DateField()


class WorkExperience(EmbeddedDocument):
    shipowner = StringField()
    type_of_vessel = StringField()
    ships_name = StringField()
    position = StringField()
    period_of_work_from = DateField()
    period_of_work_to = DateField()


class History(EmbeddedDocument):
    id = IntField()
    product = StringField()
    datetime = DateTimeField()
    sum = FloatField()
    method_of_payment = StringField()
    check = StringField()


class Payment(EmbeddedDocument):
    balance: FloatField()
    payment_history = EmbeddedDocumentField(ListField(History))
    autofill = BooleanField()



class UserModel(Document):
    email = EmailField(unique=True)
    phone_number = StringField()
    first_name = StringField()
    last_name = StringField()
    patronymic = StringField()
    country = StringField()
    region = StringField()
    city = StringField()
    telegram = StringField()
    positions = ListField(EmbeddedDocumentField(Position))
    worked = ListField(EmbeddedDocumentField(Worked))
    status = StringField()
    payment_operations = EmbeddedDocumentField(Payment)
    favorites_company = ListField(EmbeddedDocumentField(FavoritesCompany))
    favorites_vacancies = ListField(EmbeddedDocumentField(FavoritesVacancies))
    notification_settings = EmbeddedDocumentField(NotificationSettings)
    main_documents = EmbeddedDocumentField(MainDocumentsUsers)
    shipwrights_papers = EmbeddedDocumentField(ShipwrightsPapers)
    additional_documents = EmbeddedDocumentField(AdditionalDocuments)
    working_experience = EmbeddedDocumentField(WorkExperience)


class CompanyModel(Document):
    email = EmailField(unique=True)
    phone_number = StringField(unique=True)
    first_name = StringField()
    last_name = StringField()
    patronymic = StringField()
    telegram = StringField()
    company_name = StringField()
    company_inn = IntField(unique=True)
    company_address = StringField()
    favorites_resume = ListField(EmbeddedDocumentField(Favorites))
    black_list_resume = ListField(EmbeddedDocumentField(BlackList))
    vacancies = ListField(EmbeddedDocumentField(Vacancies))
    notification_settings = EmbeddedDocumentField(NotificationSettings)


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


class SwimsTariffs(Document):
    status = StringField()
    period = StringField()
    cost = IntField()


class ListDescriptionTariffs(EmbeddedDocument):
    number = IntField()
    description = StringField()


class DescriptionTariffs(Document):
    title = StringField()
    description_list = ListField(EmbeddedDocumentField(ListDescriptionTariffs))


class Tariffs(EmbeddedDocument):
    title = StringField()
    count_publications = IntField()
    count_possibilities = IntField()
    price = IntField()


class CompanyTariffs(Document):
    description = ListField(EmbeddedDocumentField(Tariffs))


load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = Starlette(
    routes=[
        Route(
            "/",
            lambda r: HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>'),
        )
    ],
    on_startup=[lambda: connect(db="aflot_backend", host="mongo", port=27017, username=DB_USERNAME,
                                password=DB_PASSWORD)],
    on_shutdown=[lambda: disconnect()],
)


# app = Starlette(
#     routes=[
#         Route(
#             "/",
#             lambda r: HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>'),
#         )
#     ],
#     on_startup=[lambda: connect(db="aflot_backend", host="localhost", port=27017)],
#     on_shutdown=[lambda: disconnect()],
# )
# Create admin
admin = Admin(title="Admin: AFLOT ADMIN")


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
admin.add_view(ModelView(SwimsTariffs, icon="fa fa-users"))
admin.add_view(ModelView(DescriptionTariffs, icon="fa fa-users"))
admin.add_view(ModelView(CompanyTariffs, icon="fa fa-users"))

admin.mount_to(app)
