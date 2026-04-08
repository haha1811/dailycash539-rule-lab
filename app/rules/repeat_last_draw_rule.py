from app.rules.base import BaseRule


class RepeatLastDrawRule(BaseRule):
    rule_id = "repeat_last_draw_rule"
    name = "Repeat Last Draw Rule"
    description = "沿用上一期號碼"

    def evaluate(self, history_draws: list[dict], config: dict | None = None) -> dict:
        if not history_draws:
            return self._empty("無歷史資料")
        nums = sorted(history_draws[-1]["numbers"])
        return {
            "rule_id": self.rule_id,
            "triggered": True,
            "candidates": nums,
            "score_map": {str(n): 1.0 for n in nums},
            "reason": "上一期號碼延續",
            "meta": {},
        }
