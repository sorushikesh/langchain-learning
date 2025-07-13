from pydantic import BaseModel

class AccountDTO(BaseModel):
    account_number: str
    account_holder: str
    current_balance: float