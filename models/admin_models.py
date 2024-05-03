from mongoengine import (Document, EmailField, IntField, StringField, DateTimeField, BooleanField, DateField,
                         EmbeddedDocument, EmbeddedDocumentField, ListField, ImageField, FloatField, FileField)
from mongoengine.fields import ObjectIdField
from beanie import PydanticObjectId
import os


class Auth(Document):
    resumeID = ObjectIdField()
    email = EmailField(unique=True)
    first_name = StringField()
    last_name = StringField()
    patronymic = StringField()
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
    responses = ListField(ObjectIdField())
    job_offers = ListField(ObjectIdField())


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
    id = ObjectIdField()
    product = StringField()
    datetime = DateTimeField()
    sum = FloatField()
    method_of_payment = StringField()
    check = StringField()


class UserModel(Document):
    email = EmailField(unique=True)
    phone_number = StringField()
    first_name = StringField()
    last_name = StringField()
    patronymic = StringField()
    photo_path = StringField()
    country = StringField()
    region = StringField()
    city = StringField()
    telegram = StringField()
    positions = ListField(EmbeddedDocumentField(Position))
    worked = ListField(EmbeddedDocumentField(Worked))
    status = StringField()
    balance = FloatField()
    autofill = BooleanField()
    payment_history = ListField(EmbeddedDocumentField(History))
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
    photo_path = StringField()
    telegram = StringField()
    company_name = StringField()
    company_inn = IntField(unique=True)
    company_address = StringField()
    favorites_resume = ListField(ObjectIdField())
    black_list_resume = ListField(ObjectIdField())
    vacancies = ListField(ObjectIdField())
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
    photo = ImageField()
    photo_path = StringField()
    view_count = IntField()

    def save(self, *args, **kwargs):
        if self.photo:
            image_data = self.photo.read()

            if not os.path.exists("images"):
                os.makedirs("images")

            object_id = PydanticObjectId()
            file_path = os.path.join("images", f"{object_id}.jpg")

            with open(file_path, "wb") as f:
                f.write(image_data)

            self.photo_path = file_path

        elif self.photo_path:
            os.remove(self.photo_path)
            self.photo_path = None

        super(NewsModel, self).save(*args, **kwargs)


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
