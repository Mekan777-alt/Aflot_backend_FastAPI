import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from mongoengine import (Document, EmailField, IntField, StringField, DateTimeField, BooleanField, DateField,
                         EmbeddedDocument, EmbeddedDocumentField, ListField, ImageField, FloatField, FileField)
from mongoengine.fields import ObjectIdField
from beanie import PydanticObjectId
import os
import requests
from dotenv import load_dotenv

load_dotenv()


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

        BUCKET_NAME = os.getenv('BUCKET_NAME')
        if self.photo:
            image_data = self.photo.read()

            access_key, secret_key = self.get_s3_credentials_for_news()

            client_s3 = boto3.client(
                's3',
                endpoint_url="https://storage.clo.ru",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )

            object_id = PydanticObjectId()
            file_key = f"news/{object_id}.jpg"

            try:
                client_s3.put_object(
                    Bucket=BUCKET_NAME,
                    Body=image_data,
                    Key=file_key,
                    ACL='public-read',
                    ContentType='image/jpeg'
                )
            except (NoCredentialsError, PartialCredentialsError) as e:

                raise RuntimeError(f"S3 credentials are invalid or not provided: {e}")

            self.photo_path = f"https://{BUCKET_NAME}.storage.clo.ru/{BUCKET_NAME}/{file_key}"

        elif self.photo_path:
            pass
            # self.delete_photo_from_s3(self.photo_path)
            # self.photo_path = None
        super(NewsModel, self).save(*args, **kwargs)

    def get_user_s3_for_news(self):

        PROJECT_ID = os.getenv('PROJECT_ID')
        TOKEN = os.getenv('TOKEN')

        url = f"https://api.clo.ru/v2/projects/{PROJECT_ID}/s3/users"

        header = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}

        r = requests.get(url, headers=header)

        if r.status_code != 200:
            return r.json()

        parse = r.json()

        return parse['result'][0]['id']

    def get_s3_credentials_for_news(self):
        object_id = self.get_user_s3_for_news()
        TOKEN = os.getenv('TOKEN')

        url = f"https://api.clo.ru/v2/s3/users/{object_id}/credentials"

        header = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}

        r = requests.get(url=url, headers=header)

        access_key, secret_key = r.json()['result'][0]['access_key'], r.json()['result'][0]['secret_key']

        return access_key, secret_key


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
