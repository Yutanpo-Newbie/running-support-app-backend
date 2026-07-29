def calculate_total_score(
    target_distance_km: float,
    actual_distance_km: float,
    elevation_gain_m: float,
    signals: int,
    intersections: int,
    traffic_score: float,
) -> float:
    distance_penalty = abs(target_distance_km - actual_distance_km) * 20
    elevation_penalty = elevation_gain_m * 0.2
    signal_penalty = signals * 2
    intersection_penalty = intersections * 1
    traffic_penalty = traffic_score * 1.5

    """
    フロントエンドでパラメータ調整の実装が完了次第、
    ユーザーの好みに応じて重みづけする内容を以下に追加する。
    """

    total_score = (
        distance_penalty
        + elevation_penalty
        + signal_penalty
        + intersection_penalty
        + traffic_penalty
    )

    return round(total_score, 2)