# NEXT STEPS

## 下一步可擴充方向

1. **Plugin Rule 架構**
   - 以 entry points / 動態載入模組方式註冊規則
   - 將 RULE_REGISTRY 改為可外掛擴充
2. **非同步回測任務**
   - 將回測改為背景任務（Celery / RQ / Dramatiq）
   - UI 顯示進度條與狀態輪詢
3. **更多評估指標**
   - 命中分布直方圖
   - 連續命中天數
   - 置信區間
4. **資料治理**
   - 匯入錯誤報告下載
   - 增加來源版本與 checksum

## 可以優化的地方

1. 規則參數驗證可改用更嚴謹 schema。
2. UI 可加入圖表（例如 hit trend）。
3. 回測 baseline 可增加固定 seed 設定提升可重現性。
4. API 回應可補分頁與排序參數。

## 如何新增第 6 條規則（範例流程）

1. 在 `app/rules/` 新增 `my_new_rule.py`，實作 `BaseRule`。
2. 保持 `evaluate(...)` 輸出格式一致。
3. 在 `app/rules/__init__.py` 註冊到 `RULE_REGISTRY`。
4. 在 `DEFAULT_RULES` 新增預設設定（is_enabled/weight/params_json）。
5. 補測試：
   - `tests/test_rules.py` 增加該規則格式與範圍測試。
   - 若有特殊整合行為，補 `tests/test_aggregator.py`。
6. 重啟服務後可在 `/rules` 直接啟用、調整權重與參數。
