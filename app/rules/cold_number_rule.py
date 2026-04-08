from app.rules.base import BaseRule, count_numbers


class ColdNumberRule(BaseRule):
    rule_id = "cold_number_rule"
    name = "Cold Number Rule"
    description = "最近 N 期低頻號碼"

    def evaluate(self, history_draws: list[dict], config: dict | None = None) -> dict:
        config = config or {}
        window_size = int(config.get("window_size", 15))
        top_n = int(config.get("top_n", 5))
        if not history_draws:
            return self._empty("無歷史資料", {"window_size": window_size, "top_n": top_n})

        recent = history_draws[-window_size:]
        counts = count_numbers(recent)
        all_counts = [(n, counts.get(n, 0)) for n in range(1, 40)]
        ranked = sorted(all_counts, key=lambda x: (x[1], x[0]))[:top_n]
        candidates = [n for n, _ in ranked]
        max_gap = max([c for _, c in ranked], default=1) + 1
        score_map = {str(n): round((max_gap - cnt) / max_gap, 4) for n, cnt in ranked}
        return {
            "rule_id": self.rule_id,
            "triggered": bool(candidates),
            "candidates": candidates,
            "score_map": score_map,
            "reason": f"最近{window_size}期冷號",
            "meta": {"window_size": window_size, "top_n": top_n},
        }
