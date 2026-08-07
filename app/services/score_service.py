from typing import List
from app.models.group import Group
from app.models.course import Course


def validate_holes(player, course: Course):
    if len(player.holes) != len(course.holes):
        raise ValueError(
            f"ホール数が一致しません: player={len(player.holes)}, course={len(course.holes)}"
        )


def sort_player_holes(player):
    player.holes = sorted(player.holes, key=lambda h: h.hole)


def calculate_scores(group: Group, course: Course):
    """
    ShareMessageGroup / PlayerShareMessage 用の
    total_score / total_diff / rank を返す新仕様ロジック
    """

    results_raw: list[dict] = []

    for player in group.players:
        sort_player_holes(player)
        validate_holes(player, course)

        # score が不正な値でないかチェック
        for h in player.holes:
            if h.score is not None and not (1 <= h.score <= 15):
                raise ValueError(f"score が不正です: hole {h.hole}")

        # 入力済みホールのみ使用（途中終了対応）
        finished_holes = [h for h in player.holes if h.score is not None]

        # 未入力のみの場合（rank は後で None にする）
        if len(finished_holes) == 0:
            results_raw.append(
                {
                    "player_name": player.player_name,
                    "total_score": None,
                    "total_diff": None,
                }
            )
            continue

        # 合計スコア
        total_score = sum(h.score for h in finished_holes)

        # 合計差分
        total_diff = sum(
            h.score - course.holes[h.hole - 1].par
            for h in finished_holes
        )

        results_raw.append(
            {
                "player_name": player.player_name,
                "total_score": total_score,
                "total_diff": total_diff,
            }
        )

    # ★ 順位付け（total_score → total_diff の昇順）
    valid = [r for r in results_raw if r["total_score"] is not None]
    invalid = [r for r in results_raw if r["total_score"] is None]

    valid = sorted(valid, key=lambda x: (x["total_score"], x["total_diff"]))

    rank = 1
    prev_score = None
    prev_diff = None

    for idx, r in enumerate(valid):
        if prev_score is not None and r["total_score"] == prev_score and r["total_diff"] == prev_diff:
            r["rank"] = rank
        else:
            rank = idx + 1
            r["rank"] = rank

        prev_score = r["total_score"]
        prev_diff = r["total_diff"]

    # 未入力は rank=None
    for r in invalid:
        r["rank"] = None

    # ★ ShareMessageGroup 用に dict のまま返す（PlayerResult は使わない）
    return valid + invalid

