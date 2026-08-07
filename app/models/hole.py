from pydantic import BaseModel

class Hole(BaseModel):
    hole: int
    par: int
    score: int | None = None
