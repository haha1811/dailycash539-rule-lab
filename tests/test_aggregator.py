from app.services.aggregator_service import aggregate_rule_outputs


def test_aggregator_score_and_accumulation():
    outputs = [
        {"rule_id": "r1", "candidates": [1, 2], "score_map": {"1": 0.8, "2": 0.3}},
        {"rule_id": "r2", "candidates": [1, 3], "score_map": {"1": 0.5, "3": 1.0}},
    ]
    weights = {"r1": 2.0, "r2": 1.0}
    rows = aggregate_rule_outputs(outputs, weights)
    top = rows[0]
    assert top["number"] == 1
    assert top["final_score"] == 2.1
    assert top["hit_by_rules_count"] == 2
