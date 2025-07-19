from datetime import datetime

from pydantic import BaseModel


class TransactionDTO(BaseModel):
    account_number: str
    transaction_amount: float
    transaction_type: str
    transaction_date: datetime
    description: str
