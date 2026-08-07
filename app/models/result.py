from pydantic import BaseModel

class PlayerResult(BaseModel):
    player_name: str
    total_score: int | None
    total_diff: int | None
    rank: int | None
