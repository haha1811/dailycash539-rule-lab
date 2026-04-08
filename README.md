# dailycash539-rule-lab

今彩 539 巧合規則驗證系統 MVP。

> 本系統用於驗證巧合規則，不保證預測效果。

## 1) 專案目的

本專案聚焦在「可驗證、可回測、可擴充」：

1. 匯入今彩 539 歷史資料（CSV）
2. 以統一規則介面執行多條規則
3. 整合規則候選號碼得到最終排序
4. 逐期回測（每期僅使用當期前歷史資料）
5. 比較 strategy 與 baseline（random / hot / cold）

## 2) 安裝方式

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) 啟動方式

```bash
uvicorn app.main:app --reload
```

開啟：http://127.0.0.1:8000

## 4) CSV 匯入格式

欄位固定：

- draw_no
- draw_date (YYYY-MM-DD)
- n1
- n2
- n3
- n4
- n5

範例檔：`data/sample_dailycash539.csv`

驗證規則：

- draw_no 唯一
- draw_date 不可空
- 同一期 5 碼不得重複
- 號碼必須在 1~39
- `numbers_sorted` 會自動產生
- 重複 draw_no 會一致地略過（計入 skipped）

## 5) 規則說明（MVP 5 條）

所有規則都實作 `BaseRule.evaluate(history_draws, config) -> dict`，輸出固定結構：
`rule_id / triggered / candidates / score_map / reason / meta`。

1. `hot_number_rule`：最近 N 期高頻號碼（預設 window=10, top_n=5）
2. `cold_number_rule`：最近 N 期低頻/未出現號碼（預設 window=15, top_n=5）
3. `repeat_last_draw_rule`：上一期 5 碼作候選
4. `tail_pattern_rule`：
   - 先統計最近 N 期尾數(0~9)頻率
   - 取最高的 top_tail_count 個尾數
   - 每個尾數從 1~39 的對應清單中取前 per_tail_pick 個號碼
   - 作為簡化版尾數策略
5. `adjacent_number_rule`：上一期每個號碼取 ±1（可用 neighbor_distance 擴大）

## 6) 回測邏輯說明

`POST /api/backtests` 建立任務後，系統會：

1. 依日期區間逐期走訪
2. 對目標期 `T` 只拿 `draw_date < T` 的資料作歷史
3. 跑所有啟用規則
4. 透過聚合器累加分數：`final_score = Σ(rule_score * rule_weight)`
5. 取 top_k 做為 strategy 預估
6. 與當期實際號碼比較計算 hit_count
7. 同期計算 baseline：
   - random_baseline: 1~39 隨機取 5 碼
   - hot_baseline: 僅 hot rule
   - cold_baseline: 僅 cold rule
8. 彙整指標：
   - 總期數
   - 平均命中
   - 命中至少 1 / 2 / 3 碼比例

## 7) API 與 UI

### API

- `POST /api/draws/import`
- `GET /api/rules`
- `PUT /api/rules/{rule_id}`
- `GET /api/predictions/latest`
- `POST /api/backtests`
- `GET /api/backtests`
- `GET /api/backtests/{id}`
- `GET /api/backtests/{id}/results`

### UI

- `/` 首頁
- `/draws` 歷史資料（最近 20 期）
- `/draws/import` 匯入頁
- `/rules` 規則管理
- `/predictions/latest` 最新預估
- `/backtests` 回測摘要列表

## 8) 測試

```bash
pytest
```

涵蓋：

- 5 條規則輸出格式/範圍
- 聚合器分數與累加
- 回測流程可運作、含 baseline 摘要

## 9) 聲明

- 本系統不是保證中獎工具。
- 本系統不是投資或下注建議。
- 目的為規則驗證與歷史回測研究。
