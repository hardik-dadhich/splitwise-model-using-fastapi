from pydantic import BaseModel
from typing import List

class Group(BaseModel):
    # The Group to whom user Associate with
    name: str
    userlist:  List[str]
    