from app.rules.base import BaseRule


class AdjacentNumberRule(BaseRule):
    rule_id = "adjacent_number_rule"
    name = "Adjacent Number Rule"
    description = "上一期號碼相鄰數"

    def evaluate(self, history_draws: list[dict], config: dict | None = None) -> dict:
        config = config or {}
        dist = int(config.get("neighbor_distance", 1))
        if not history_draws:
            return self._empty("無歷史資料", {"neighbor_distance": dist})

        last_numbers = history_draws[-1]["numbers"]
        cands = set()
        for n in last_numbers:
            for d in range(1, dist + 1):
                if 1 <= n - d <= 39:
                    cands.add(n - d)
                if 1 <= n + d <= 39:
                    cands.add(n + d)

        candidates = sorted(cands)
        return {
            "rule_id": self.rule_id,
            "triggered": bool(candidates),
            "candidates": candidates,
            "score_map": {str(n): 1.0 for n in candidates},
            "reason": "上一期相鄰號",
            "meta": {"neighbor_distance": dist},
        }
