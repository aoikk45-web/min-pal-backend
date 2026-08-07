from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class ShareMode(str, Enum):
    detail = "detail"
    simple = "simple"
    emoji = "emoji"

class HoleData(BaseModel):
    hole: int
    par: int
    score: Optional[int]   # 未入力は None
    diff: Optional[int]    # score=None のとき None

class PlayerShareMessage(BaseModel):
    player_name: str
    holes: List[HoleData]
    total_score: Optional[int]   # 未入力プレイヤーは None
    total_diff: Optional[int]    # 未入力プレイヤーは None
    rank: Optional[int]          # 未入力プレイヤーは None
    text: str                    # 共有テキスト

class ShareMessageGroup(BaseModel):
    course_name: str
    mode: ShareMode
    messages: List[PlayerShareMessage]
    ranking_text: str
    ranking_emoji: Optional[str] = None



