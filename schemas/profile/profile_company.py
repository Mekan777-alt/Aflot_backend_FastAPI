from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union


class CompanyNotification(BaseModel):
    send_email: bool
    send_sms: bool
    send_telegram: bool
    mailing_notification: Optional[bool]


class CompanyOldSettings(BaseModel):
    email: EmailStr
    phone_number: str
    telegram: Optional[str]
    notification_settings: Optional[CompanyNotification]


