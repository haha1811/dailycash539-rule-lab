from app.rules import RULE_REGISTRY


def fake_history(n=20):
    rows = []
    for i in range(1, n + 1):
        nums = [((i + j - 1) % 39) + 1 for j in range(5)]
        rows.append({"id": i, "draw_date": f"2025-01-{i:02d}", "numbers": nums})
    return rows


def assert_rule_output(out):
    assert set(["rule_id", "triggered", "candidates", "score_map", "reason", "meta"]).issubset(out.keys())
    for n in out["candidates"]:
        assert 1 <= n <= 39
    assert isinstance(out["score_map"], dict)
    for k, v in out["score_map"].items():
        assert str(int(k)) == k
        assert isinstance(v, (int, float))


def test_all_rule_output_format():
    history = fake_history()
    for _, rule in RULE_REGISTRY.items():
        out = rule.evaluate(history, {})
        assert_rule_output(out)
