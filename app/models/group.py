from pydantic import BaseModel
from typing import List
from .player import Player

class Group(BaseModel):
    players: List[Player]
