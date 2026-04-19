# 線上算命系統 — 路由設計文件

> **版本：** v1.0
> **建立日期：** 2026-04-19
> **狀態：** 草稿
> **依據：** [PRD v1.0](./PRD.md) ／ [ARCHITECTURE v1.0](./ARCHITECTURE.md) ／ [DB_DESIGN v1.0](./DB_DESIGN.md)

---

## 目錄

- [1. 路由總覽表格](#1-路由總覽表格)
- [2. 每個路由的詳細說明](#2-每個路由的詳細說明)
- [3. Jinja2 模板清單](#3-jinja2-模板清單)
- [4. 路由骨架對照表](#4-路由骨架對照表)

---

## 1. 路由總覽表格

### 1.1 首頁與每日運勢（main_bp）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 首頁 | GET | `/` | `index.html` | 顯示每日運勢 + 算命方式導覽卡片 |

### 1.2 抽籤功能（fortune_bp，URL 前綴：`/fortune`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 抽籤頁面 | GET | `/fortune/draw` | `fortune/draw.html` | 顯示選擇類別頁面 |
| 執行抽籤 | POST | `/fortune/draw` | `fortune/result.html` | 隨機抽籤、儲存結果、顯示籤詩 |

### 1.3 塔羅占卜功能（tarot_bp，URL 前綴：`/tarot`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 選擇主題與牌陣 | GET | `/tarot/select` | `tarot/select.html` | 顯示主題與牌陣選擇頁面 |
| 執行占卜 | POST | `/tarot/select` | `tarot/result.html` | 隨機抽牌、儲存結果、顯示解讀 |

### 1.4 擲筊功能（bwa_bp，URL 前綴：`/bwa`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 擲筊頁面 | GET | `/bwa/throw` | `bwa/throw.html` | 顯示輸入問題頁面 |
| 執行擲筊 | POST | `/bwa/throw` | `bwa/result.html` | 隨機擲筊、儲存結果、顯示結果 |

### 1.5 歷史紀錄功能（history_bp，URL 前綴：`/history`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 歷史紀錄列表 | GET | `/history` | `history/index.html` | 顯示所有算命紀錄（支援篩選） |
| 刪除紀錄 | POST | `/history/delete/<id>` | — | 刪除指定紀錄後重導向到列表 |

### 1.6 捐香油錢功能（donation_bp，URL 前綴：`/donation`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 捐款頁面 | GET | `/donation` | `donation/index.html` | 顯示香油錢捐款頁面 |
| 執行捐款 | POST | `/donation` | `donation/thanks.html` | 模擬捐款、儲存紀錄、顯示感謝 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁（main_bp）

#### `GET /`

- **輸入：** 無
- **處理邏輯：**
  1. 根據系統日期產生每日運勢（幸運色、幸運數字、運勢星級、一句話建議）
  2. 使用日期作為隨機種子，確保同一天內容一致
- **輸出：** 渲染 `index.html`，傳入每日運勢資料
- **錯誤處理：** 無特殊錯誤情境

---

### 2.2 抽籤功能（fortune_bp）

#### `GET /fortune/draw`

- **輸入：** 無
- **處理邏輯：** 準備類別選項列表（綜合運勢、感情、事業、學業、財運、健康）
- **輸出：** 渲染 `fortune/draw.html`，傳入可選類別
- **錯誤處理：** 無特殊錯誤情境

#### `POST /fortune/draw`

- **輸入：** 表單欄位 `category`（籤詩類別）
- **處理邏輯：**
  1. 驗證 `category` 是否為有效類別
  2. 呼叫 `Fortune.get_random_by_category(category)` 隨機抽取一支籤
  3. 呼叫 `History.create(type_='fortune', category=category, result_summary=level, result_detail=json)` 儲存結果
- **輸出：** 渲染 `fortune/result.html`，傳入籤詩資料
- **錯誤處理：**
  - 類別無效 → 重導向回 `/fortune/draw` 並顯示錯誤訊息
  - 該類別無籤詩 → 顯示「暫無籤詩」提示

---

### 2.3 塔羅占卜功能（tarot_bp）

#### `GET /tarot/select`

- **輸入：** 無
- **處理邏輯：** 準備主題選項（愛情、事業、人際、當日運勢）與牌陣選項（單張牌、三張牌）
- **輸出：** 渲染 `tarot/select.html`，傳入選項列表
- **錯誤處理：** 無特殊錯誤情境

#### `POST /tarot/select`

- **輸入：** 表單欄位 `topic`（主題）、`spread`（牌陣：`single` 或 `three`）
- **處理邏輯：**
  1. 驗證 `topic` 與 `spread` 是否有效
  2. 根據牌陣數量呼叫 `Tarot.get_random(count)` 抽取塔羅牌
  3. 每張牌隨機決定正位/逆位
  4. 呼叫 `History.create(type_='tarot', category=topic, result_summary=牌名, result_detail=json)` 儲存結果
- **輸出：** 渲染 `tarot/result.html`，傳入塔羅牌資料
- **錯誤處理：**
  - 主題或牌陣無效 → 重導向回 `/tarot/select` 並顯示錯誤訊息
  - 資料庫中無塔羅牌 → 顯示「暫無牌面資料」提示

---

### 2.4 擲筊功能（bwa_bp）

#### `GET /bwa/throw`

- **輸入：** 無
- **處理邏輯：** 無
- **輸出：** 渲染 `bwa/throw.html`
- **錯誤處理：** 無特殊錯誤情境

#### `POST /bwa/throw`

- **輸入：** 表單欄位 `question`（使用者的是非問題）
- **處理邏輯：**
  1. 驗證 `question` 不為空
  2. 隨機產生擲筊結果：聖筊（一正一反）、笑筊（兩正面）、怒筊（兩反面）
  3. 呼叫 `History.create(type_='bwa', question=question, result_summary=結果名稱, result_detail=json)` 儲存結果
- **輸出：** 渲染 `bwa/result.html`，傳入擲筊結果與問題
- **錯誤處理：**
  - 問題為空 → 重導向回 `/bwa/throw` 並顯示錯誤訊息

---

### 2.5 歷史紀錄功能（history_bp）

#### `GET /history`

- **輸入：** 查詢參數 `type`（可選，篩選類型）、`date`（可選，篩選日期）
- **處理邏輯：**
  1. 若有 `type` 參數 → 呼叫 `History.get_by_type(type_)`
  2. 否則 → 呼叫 `History.get_all()`
  3. 若有 `date` 參數 → 在結果中過濾日期
- **輸出：** 渲染 `history/index.html`，傳入紀錄列表與目前的篩選條件
- **錯誤處理：** 無特殊錯誤情境

#### `POST /history/delete/<int:id>`

- **輸入：** URL 參數 `id`（紀錄 ID）
- **處理邏輯：**
  1. 呼叫 `History.delete(id)` 刪除指定紀錄
- **輸出：** 重導向到 `/history`
- **錯誤處理：**
  - 紀錄不存在 → 顯示 flash 訊息「紀錄不存在」，重導向回 `/history`

---

### 2.6 捐香油錢功能（donation_bp）

#### `GET /donation`

- **輸入：** 無
- **處理邏輯：**
  1. 呼叫 `Donation.get_total()` 取得歷史總捐款金額（用於顯示）
- **輸出：** 渲染 `donation/index.html`，傳入總捐款金額
- **錯誤處理：** 無特殊錯誤情境

#### `POST /donation`

- **輸入：** 表單欄位 `amount`（捐款金額）、`message`（可選，祈願留言）
- **處理邏輯：**
  1. 驗證 `amount` 為正整數
  2. 呼叫 `Donation.create(amount, message)` 儲存捐款紀錄
- **輸出：** 渲染 `donation/thanks.html`，傳入捐款金額與祝福語
- **錯誤處理：**
  - 金額無效（非正整數）→ 重導向回 `/donation` 並顯示錯誤訊息

---

## 3. Jinja2 模板清單

> 所有模板皆繼承 `base.html` 基礎模板。

| 模板檔案 | 繼承 | 用途 |
|----------|------|------|
| `base.html` | — | 基礎模板：共用 header、footer、導覽列、CSS/JS 引入 |
| `index.html` | `base.html` | 首頁：每日運勢 + 功能導覽卡片 |
| `fortune/draw.html` | `base.html` | 抽籤頁面：選擇類別、搖籤筒動畫 |
| `fortune/result.html` | `base.html` | 籤詩結果頁面：顯示籤等級、籤詩、解讀 |
| `tarot/select.html` | `base.html` | 塔羅選擇頁面：選擇主題與牌陣 |
| `tarot/result.html` | `base.html` | 塔羅結果頁面：翻牌動畫、牌面與解讀 |
| `bwa/throw.html` | `base.html` | 擲筊頁面：輸入問題、擲筊按鈕 |
| `bwa/result.html` | `base.html` | 擲筊結果頁面：筊杯結果與說明 |
| `history/index.html` | `base.html` | 歷史紀錄列表：所有算命紀錄、篩選、刪除 |
| `donation/index.html` | `base.html` | 捐香油錢頁面：選擇金額、輸入留言 |
| `donation/thanks.html` | `base.html` | 捐款感謝頁面：感謝動畫與祝福語 |

---

## 4. 路由骨架對照表

| Blueprint | 檔案路徑 | URL 前綴 |
|-----------|----------|----------|
| `main_bp` | `app/routes/main.py` | `/` |
| `fortune_bp` | `app/routes/fortune.py` | `/fortune` |
| `tarot_bp` | `app/routes/tarot.py` | `/tarot` |
| `bwa_bp` | `app/routes/bwa.py` | `/bwa` |
| `history_bp` | `app/routes/history.py` | `/history` |
| `donation_bp` | `app/routes/donation.py` | `/donation` |

> 路由骨架程式碼請參考 `app/routes/` 中的各檔案。

---

> 📌 **下一步：** 路由設計確認無誤後，進入 **階段六：程式碼實作**（使用 `/implementation` skill）。
