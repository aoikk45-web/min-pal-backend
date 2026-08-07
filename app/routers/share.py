from fastapi import APIRouter
from typing import Annotated
import json
import os

from app.models.group import Group
from app.models.course import Course
from app.models.share_message import (
    ShareMode,
    ShareMessageGroup,
    PlayerShareMessage,
)
from backend.app.services.score_service import calculate_scores
from backend.app.services.share_service import (
    generate_detail_message,
    generate_simple_message,
    generate_emoji_message,
    generate_ranking_text,
    generate_ranking_emoji,
)

router = APIRouter()


def load_courses() -> list[Course]:
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "..", "courses.json")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Course(**course) for course in data["courses"]]


def load_course_by_name(name: str) -> Course:
    name = name.strip()
    courses = load_courses()

    matches = [c for c in courses if c.course_name == name]
    if len(matches) == 0:
        raise ValueError(f"コースが見つかりません: {name}")
    if len(matches) > 1:
        raise ValueError(f"コース名が重複しています: {name}")

    course = matches[0]

    for h in course.holes:
        if not (1 <= h.par <= 5):
            raise ValueError(f"PAR が不正です: hole {h.hole}")

    return course


@router.post("/share", response_model=ShareMessageGroup)
def share(
    group: Group,
    course_name: Annotated[str, "コース名"],
    mode: ShareMode = ShareMode.detail,
):
    course = load_course_by_name(course_name)

    # ★ 新仕様の calculate_scores（dict の list）
    results = calculate_scores(group, course)

    messages: list[PlayerShareMessage] = []

    for r in results:
        player = next(p for p in group.players if p.player_name == r["player_name"])

        # ★ 全ホールを holes_data に入れる（未入力は None）
        holes_data = []
        for h in player.holes:
            par = course.holes[h.hole - 1].par
            score = h.score
            diff = None if score is None else score - par

            holes_data.append(
                {
                    "hole": h.hole,
                    "par": par,
                    "score": score,
                    "diff": diff,
                }
            )

        total_score = r["total_score"]
        total_diff = r["total_diff"]
        rank = r["rank"]

        # ★ 共有テキスト生成（新仕様）
        if mode == ShareMode.detail:
            text = generate_detail_message(player, course, total_score, total_diff, rank)
        elif mode == ShareMode.simple:
            text = generate_simple_message(player.player_name, total_score, total_diff, rank)
        elif mode == ShareMode.emoji:
            text = generate_emoji_message(player, course, total_score, total_diff, rank)

        messages.append(
            PlayerShareMessage(
                player_name=player.player_name,
                holes=holes_data,
                total_score=total_score,
                total_diff=total_diff,
                rank=rank,
                text=text,
            )
        )

    ranking_text = generate_ranking_text(messages)
    ranking_emoji = generate_ranking_emoji(messages) if mode == ShareMode.emoji else None

    return ShareMessageGroup(
        course_name=course.course_name,
        mode=mode,
        messages=messages,
        ranking_text=ranking_text,
        ranking_emoji=ranking_emoji,
    )




