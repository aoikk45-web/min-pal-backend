from pydantic import BaseModel
from typing import List
from .hole import Hole

class Player(BaseModel):
    player_name: str
    holes: List[Hole]
