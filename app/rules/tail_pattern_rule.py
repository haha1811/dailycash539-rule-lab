from collections import Counter

from app.rules.base import BaseRule


class TailPatternRule(BaseRule):
    rule_id = "tail_pattern_rule"
    name = "Tail Pattern Rule"
    description = "分析常見尾數"

    def evaluate(self, history_draws: list[dict], config: dict | None = None) -> dict:
        config = config or {}
        window_size = int(config.get("window_size", 12))
        top_tail_count = int(config.get("top_tail_count", 2))
        per_tail_pick = int(config.get("per_tail_pick", 2))
        if not history_draws:
            return self._empty("無歷史資料")

        recent = history_draws[-window_size:]
        tail_counter = Counter()
        for d in recent:
            tail_counter.update([n % 10 for n in d["numbers"]])

        top_tails = [t for t, _ in tail_counter.most_common(top_tail_count)]
        candidates = []
        for tail in top_tails:
            bucket = [n for n in range(1, 40) if n % 10 == tail]
            candidates.extend(bucket[:per_tail_pick])

        unique_candidates = sorted(set(candidates))
        max_count = max([tail_counter[t] for t in top_tails], default=1)
        score_map = {str(n): round(tail_counter[n % 10] / max_count, 4) for n in unique_candidates}
        return {
            "rule_id": self.rule_id,
            "triggered": bool(unique_candidates),
            "candidates": unique_candidates,
            "score_map": score_map,
            "reason": "近期尾數模式",
            "meta": {
                "window_size": window_size,
                "top_tail_count": top_tail_count,
                "per_tail_pick": per_tail_pick,
                "top_tails": top_tails,
            },
        }
