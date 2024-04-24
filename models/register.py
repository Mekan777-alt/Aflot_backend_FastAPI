from datetime import date
from beanie import Document
from schemas.auth.auth import Optional, Worked, Position
from models.db import db
from pydantic import BaseModel, EmailStr, Field
from typing import List
from beanie import PydanticObjectId, Indexed


class NotificationSettings(BaseModel):
    send_email: bool = False
    send_sms: bool = False
    send_telegram: bool = False
    mailing_notification: bool = False


class Vacancies(BaseModel):
    id: PydanticObjectId


class BlackList(BaseModel):
    id: PydanticObjectId


class FavoritesSailor(BaseModel):
    id: PydanticObjectId


class FavoritesCompany(BaseModel):
    id: PydanticObjectId


class FavoritesVacancies(BaseModel):
    id: PydanticObjectId


class MainDocumentsUsers(BaseModel):
    foreign_passport: Optional[date] = None
    seafarers_ID_card: Optional[date] = None
    diploma: Optional[date] = None
    initial_safety_training: Optional[date] = None
    designated_safeguarding_responsibilities: Optional[date] = None
    dinghy_and_raft_specialist: Optional[date] = None
    fighting_fire_with_an_expanded_program: Optional[date] = None
    providing_first_aid: Optional[date] = None
    prevention_of_marine_pollution: Optional[date] = None
    tanker_certificate: Optional[date] = None
    occupational_health_and_safety: Optional[date] = None
    medical_commission: Optional[date] = None


class ShipwrightsPapers(BaseModel):
    gmssb: Optional[date] = None
    eknis: Optional[date] = None
    rlt: Optional[date] = None
    sarp: Optional[date] = None


class AdditionalDocuments(BaseModel):
    isolation_breathing_apparatus: Optional[date] = None
    naval_training: Optional[date] = None
    transportation_safety: Optional[date] = None
    tanker_certificate: Optional[date] = None


class WorkExperience(BaseModel):
    shipowner: Optional[str] = None
    type_of_vessel: Optional[str] = None
    ships_name: Optional[str] = None
    position: Optional[str] = None
    period_of_work_from: Optional[date] = None
    period_of_work_to: Optional[date] = None


class user_model(Document):
    __database__ = db

    id: PydanticObjectId = Field(None, alias="_id")
    email: Indexed(EmailStr, unique=True)
    phone_number: Indexed(str, unique=True)
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    telegram: Optional[str] = None
    positions: Optional[List[Position]] = None
    worked: Optional[List[Worked]] = None
    status: Optional[str] = None
    favorites_company: Optional[List[FavoritesCompany]] = None
    favorites_vacancies: Optional[List[FavoritesVacancies]] = None
    notification_settings: NotificationSettings
    main_documents: Optional[MainDocumentsUsers] = None
    shipwrights_papers: Optional[ShipwrightsPapers] = None
    additional_documents: Optional[AdditionalDocuments] = None
    working_experience: Optional[WorkExperience] = None

    async def create_default(self):
        self.main_documents = MainDocumentsUsers(
            foreign_passport=None,
            seafarers_ID_card=None,
            diploma=None,
            initial_safety_training=None,
            designated_safeguarding_responsibilities=None,
            dinghy_and_raft_specialist=None,
            fighting_fire_with_an_expanded_program=None,
            providing_first_aid=None,
            prevention_of_marine_pollution=None,
            tanker_certificate=None,
            occupational_health_and_safety=None,
            medical_commission=None,
        )

        self.shipwrights_papers = ShipwrightsPapers(
            gmssb=None,
            eknis=None,
            rlt=None,
            sarp=None,
        )

        self.additional_documents = AdditionalDocuments(
            isolation_breathing_apparatus=None,
            naval_training=None,
            transportation_safety=None,
            tanker_certificate=None,
        )

        self.working_experience = WorkExperience(
            shipowner=None,
            type_of_vessel=None,
            ships_name=None,
            position=None,
            period_of_work_from=None,
            period_of_work_to=None,
        )


class company_model(Document):
    __database__ = db

    id: PydanticObjectId = Field(None, alias="_id")
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    telegram: Optional[str] = None
    company_name: str
    company_inn: Indexed(int, unique=True)
    company_address: str
    favorites_resume: Optional[List[FavoritesSailor]] = None
    black_list_resume: Optional[List[BlackList]] = None
    vacancies: Optional[List[Vacancies]] = None
    notification_settings: NotificationSettings
