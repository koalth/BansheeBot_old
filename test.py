from pydantic import BaseModel
from typing import List


class Pet(BaseModel):
    name: str


class Person(BaseModel):
    name: str
    age: int
    pets: List[Pet]
