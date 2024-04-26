from pydantic import BaseModel


class PaymentDetails(BaseModel):
    balance: float
    autofill: bool
    count_history: int
