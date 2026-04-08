from app.rules.adjacent_number_rule import AdjacentNumberRule
from app.rules.cold_number_rule import ColdNumberRule
from app.rules.hot_number_rule import HotNumberRule
from app.rules.repeat_last_draw_rule import RepeatLastDrawRule
from app.rules.tail_pattern_rule import TailPatternRule

RULE_REGISTRY = {
    HotNumberRule.rule_id: HotNumberRule(),
    ColdNumberRule.rule_id: ColdNumberRule(),
    RepeatLastDrawRule.rule_id: RepeatLastDrawRule(),
    TailPatternRule.rule_id: TailPatternRule(),
    AdjacentNumberRule.rule_id: AdjacentNumberRule(),
}

DEFAULT_RULES = [
    {
        "rule_id": "hot_number_rule",
        "name": "Hot Number Rule",
        "description": "最近 N 期高頻號碼",
        "is_enabled": True,
        "weight": 1.0,
        "params_json": {"window_size": 10, "top_n": 5},
    },
    {
        "rule_id": "cold_number_rule",
        "name": "Cold Number Rule",
        "description": "最近 N 期低頻號碼",
        "is_enabled": True,
        "weight": 1.0,
        "params_json": {"window_size": 15, "top_n": 5},
    },
    {
        "rule_id": "repeat_last_draw_rule",
        "name": "Repeat Last Draw Rule",
        "description": "沿用上一期號碼",
        "is_enabled": True,
        "weight": 0.8,
        "params_json": {},
    },
    {
        "rule_id": "tail_pattern_rule",
        "name": "Tail Pattern Rule",
        "description": "分析常見尾數",
        "is_enabled": True,
        "weight": 0.9,
        "params_json": {"window_size": 12, "top_tail_count": 2, "per_tail_pick": 2},
    },
    {
        "rule_id": "adjacent_number_rule",
        "name": "Adjacent Number Rule",
        "description": "上一期號碼相鄰數",
        "is_enabled": True,
        "weight": 0.7,
        "params_json": {"neighbor_distance": 1},
    },
]
