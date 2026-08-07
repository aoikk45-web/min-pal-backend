from typing import List
from backend.app.models.player import Player
from backend.app.models.course import Course
from backend.app.models.share_message import (
    HoleData,
    PlayerShareMessage,
    ShareMessageGroup,
    ShareMode,
)


# 絵文字判定（18H＋⚠️対応）
def hole_emoji(score: int | None, par: int) -> str:
    if score is None:
        return "⚠️"
    return "⭕️" if score <= par else "❌"


# detail モード（表形式）
def generate_detail_message(player: Player, course: Course, total_score: int, total_diff: int, rank: int) -> str:
    table = "HOLE | PAR | SCORE | +/-\n"
    table += "-------------------------\n"

    for h, c in zip(player.holes, course.holes):
        score_text = "未入力" if h.score is None else str(h.score)
        diff_text = "-" if h.score is None else f"{h.score - c.par:+d}"

        table += f"{h.hole:<4}| {c.par:<4}| {score_text:<7}| {diff_text}\n"

    text = (
        f"▼ {player.player_name}\n"
        f"{table}\n"
        f"差分合計：{total_diff}\n"
        f"合計：{total_score}（{total_diff:+d}）\n"
        f"順位：{rank}位\n"
    )
    return text


# simple モード（合計・±・順位のみ）
def generate_simple_message(player_name: str, total_score: int, total_diff: int, rank: int | None) -> str:
    if rank is None:
        return f"{player_name}：未入力あり／順位なし"
    return f"{player_name}：{total_score}（{total_diff:+d}）／{rank}位"


# emoji モード（18H折り返し＋⚠️対応）
def generate_emoji_message(player: Player, course: Course, total_score: int, total_diff: int, rank: int | None) -> str:
    if rank is None:
        return f"⚠️ {player.player_name}（未入力あり）\nコース：{course.course_name}"

    icons = [hole_emoji(h.score, c.par) for h, c in zip(player.holes, course.holes)]

    # 18H → 9H × 2行
    hole_lines = ["".join(icons[i:i+9]) for i in range(0, len(icons), 9)]
    holes_text = "\n".join(hole_lines)

    text = (
        f"⛳ {player.player_name}（{rank}位）\n"
        f"合計：{total_score}（{total_diff:+d}）\n\n"
        f"📊 ホール結果：\n{holes_text}\n\n"
        f"🏁 コース：{course.course_name}"
    )
    return text


# グループ順位（テキスト）
def generate_ranking_text(messages: List[PlayerShareMessage]) -> str:
    lines = ["【グループ順位表】"]
    for m in messages:
        if m.rank is None:
            lines.append(f"- {m.player_name}（未入力あり）")
        else:
            lines.append(f"{m.rank}位：{m.player_name}（{m.total_score}／{m.total_diff:+d}）")
    return "\n".join(lines)


# グループ順位（絵文字）
def generate_ranking_emoji(messages: List[PlayerShareMessage]) -> str:
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}
    lines = ["🏆【順位】"]

    for m in messages:
        if m.rank is None:
            lines.append(f"⚠️ {m.player_name}（未入力あり）")
        else:
            icon = medal.get(m.rank, "🎖️")
            lines.append(f"{icon} {m.player_name}（{m.total_score}）")

    return "\n".join(lines)


