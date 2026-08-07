from pydantic import BaseModel
from typing import List
from .hole import Hole

class Course(BaseModel):
    course_name: str
    holes: List[Hole]
