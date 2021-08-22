from pydantic import BaseModel

class User(BaseModel):
    # Assuming the name would be unique
    name: str

class Balance(BaseModel):
    user: User 
    balance: float
