from pydantic import BaseModel
from typing import List
from app.models.users import User

import enum

class TypeofExpense(enum.Enum):
    EQUALS = "equals"
    PERCENTAGE = "percentage"
    RATIO = "ratio"


class Expense(BaseModel):
    # The Expense class
    user: List
    amount: int
    paidBy: str
    expensetype : TypeofExpense
    

