from abc import ABC, abstractmethod
from collections import Counter


class BaseRule(ABC):
    rule_id: str
    name: str
    description: str

    @abstractmethod
    def evaluate(self, history_draws: list[dict], config: dict | None = None) -> dict:
        raise NotImplementedError

    def _empty(self, reason: str, meta: dict | None = None) -> dict:
        return {
            "rule_id": self.rule_id,
            "triggered": False,
            "candidates": [],
            "score_map": {},
            "reason": reason,
            "meta": meta or {},
        }


def count_numbers(draws: list[dict]) -> Counter:
    c = Counter()
    for d in draws:
        c.update(d["numbers"])
    return c
