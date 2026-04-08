def aggregate_rule_outputs(rule_outputs: list[dict], weights: dict[str, float]) -> list[dict]:
    score_board: dict[int, dict] = {}
    for output in rule_outputs:
        rule_id = output["rule_id"]
        weight = weights.get(rule_id, 1.0)
        for n in output.get("candidates", []):
            score = float(output.get("score_map", {}).get(str(n), 0.0))
            if n not in score_board:
                score_board[n] = {
                    "number": n,
                    "final_score": 0.0,
                    "hit_by_rules_count": 0,
                    "rule_sources": [],
                }
            score_board[n]["final_score"] += score * weight
            if rule_id not in score_board[n]["rule_sources"]:
                score_board[n]["rule_sources"].append(rule_id)
                score_board[n]["hit_by_rules_count"] += 1

    rows = list(score_board.values())
    for row in rows:
        row["final_score"] = round(row["final_score"], 6)
        row["rule_sources"].sort()
    rows.sort(key=lambda x: (-x["final_score"], x["number"]))
    return rows
