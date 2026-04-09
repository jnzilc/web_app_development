# 線上算命系統 — 流程圖文件

> **版本：** v1.0
> **建立日期：** 2026-04-09
> **狀態：** 草稿
> **依據：** [PRD v1.0](./PRD.md) ／ [ARCHITECTURE v1.0](./ARCHITECTURE.md)

---

## 目錄

- [1. 使用者流程圖（User Flow）](#1-使用者流程圖user-flow)
- [2. 系統序列圖（Sequence Diagram）](#2-系統序列圖sequence-diagram)
- [3. 功能清單對照表](#3-功能清單對照表)

---

## 1. 使用者流程圖（User Flow）

> 描述使用者從進入網站開始，到使用各項功能的完整操作路徑。

### 1.1 整體導覽流程

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B["首頁\n（每日運勢 + 功能導覽）"]
    B --> C{要使用哪個功能？}
    C -->|抽籤| D[抽籤頁面]
    C -->|塔羅占卜| E[塔羅占卜頁面]
    C -->|擲筊| F[擲筊頁面]
    C -->|歷史紀錄| G[歷史紀錄頁面]
    C -->|捐香油錢| H[捐香油錢頁面]
```

### 1.2 抽籤（求籤）流程

```mermaid
flowchart LR
    A([進入抽籤頁面]) --> B{選擇求籤類別}
    B -->|綜合運勢| C[點擊「抽籤」按鈕]
    B -->|感情| C
    B -->|事業| C
    B -->|學業| C
    B -->|財運| C
    B -->|健康| C
    C --> D["搖籤筒動畫"]
    D --> E["顯示籤詩結果\n（等級＋籤詩＋解讀）"]
    E --> F{下一步？}
    F -->|再抽一次| B
    F -->|查看歷史| G[歷史紀錄頁面]
    F -->|回首頁| H[首頁]
```

### 1.3 塔羅牌占卜流程

```mermaid
flowchart LR
    A([進入塔羅占卜頁面]) --> B{選擇占卜主題}
    B -->|愛情| C{選擇牌陣}
    B -->|事業| C
    B -->|人際| C
    B -->|當日運勢| C
    C -->|單張牌| D["點擊翻牌"]
    C -->|三張牌| D
    D --> E["顯示牌面動畫"]
    E --> F["顯示塔羅解讀\n（牌名＋正逆位＋含義）"]
    F --> G{下一步？}
    G -->|重新占卜| B
    G -->|查看歷史| H[歷史紀錄頁面]
    G -->|回首頁| I[首頁]
```

### 1.4 擲筊流程

```mermaid
flowchart LR
    A([進入擲筊頁面]) --> B["輸入是非問題"]
    B --> C["點擊「擲筊」按鈕"]
    C --> D["筊杯翻轉動畫"]
    D --> E{擲筊結果}
    E -->|一正一反| F["聖筊 ✅\n（神明同意）"]
    E -->|兩正面| G["笑筊 😄\n（神明在笑）"]
    E -->|兩反面| H["怒筊 ❌\n（神明不同意）"]
    F --> I{下一步？}
    G --> I
    H --> I
    I -->|再擲一次| B
    I -->|查看歷史| J[歷史紀錄頁面]
    I -->|回首頁| K[首頁]
```

### 1.5 歷史紀錄流程

```mermaid
flowchart LR
    A([進入歷史紀錄頁面]) --> B["顯示所有算命紀錄列表"]
    B --> C{要執行什麼操作？}
    C -->|篩選| D{選擇篩選條件}
    D -->|依日期| E["篩選結果"]
    D -->|依類型| E
    C -->|查看詳情| F["檢視單筆紀錄詳細內容"]
    C -->|刪除紀錄| G["確認刪除"]
    G --> H["刪除成功，重新載入列表"]
    E --> B
    F --> B
    H --> B
```

### 1.6 捐香油錢流程

```mermaid
flowchart LR
    A([進入捐香油錢頁面]) --> B{選擇捐款金額}
    B -->|10 元| C["確認捐款"]
    B -->|50 元| C
    B -->|100 元| C
    B -->|500 元| C
    B -->|自訂金額| D["輸入自訂金額"] --> C
    C --> E["模擬捐款處理"]
    E --> F["顯示感謝動畫與祝福語"]
    F --> G{下一步？}
    G -->|再捐一次| B
    G -->|回首頁| H[首頁]
```

---

## 2. 系統序列圖（Sequence Diagram）

> 描述使用者操作時，資料在「瀏覽器 → Flask Route → Model → SQLite」之間的完整流動過程。

### 2.1 抽籤序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 進入抽籤頁面
    Browser->>Flask: GET /fortune/draw
    Flask-->>Browser: 渲染 draw.html（選擇類別）

    User->>Browser: 選擇類別，點擊「抽籤」
    Browser->>Flask: POST /fortune/draw
    Flask->>Model: 隨機抽取一支籤詩
    Model->>DB: SELECT 隨機籤詩 FROM fortunes
    DB-->>Model: 回傳籤詩資料
    Model-->>Flask: 回傳籤詩物件

    Flask->>Model: 儲存算命結果
    Model->>DB: INSERT INTO history
    DB-->>Model: 儲存成功
    Model-->>Flask: 確認完成

    Flask-->>Browser: 渲染 result.html（籤詩結果）
    Browser-->>User: 顯示籤詩內容與解讀
```

### 2.2 塔羅牌占卜序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 進入塔羅占卜頁面
    Browser->>Flask: GET /tarot/select
    Flask-->>Browser: 渲染 select.html（選擇主題與牌陣）

    User->>Browser: 選擇主題與牌陣，點擊「開始占卜」
    Browser->>Flask: POST /tarot/select
    Flask->>Model: 隨機抽取塔羅牌
    Model->>DB: SELECT 隨機牌面 FROM tarots
    DB-->>Model: 回傳牌面資料
    Model-->>Flask: 回傳塔羅牌物件（含正逆位）

    Flask->>Model: 儲存占卜結果
    Model->>DB: INSERT INTO history
    DB-->>Model: 儲存成功
    Model-->>Flask: 確認完成

    Flask-->>Browser: 渲染 result.html（塔羅解讀）
    Browser-->>User: 顯示牌面、牌名與解讀
```

### 2.3 擲筊序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 進入擲筊頁面
    Browser->>Flask: GET /bwa/throw
    Flask-->>Browser: 渲染 throw.html（輸入問題）

    User->>Browser: 輸入問題，點擊「擲筊」
    Browser->>Flask: POST /bwa/throw
    Flask->>Flask: 隨機產生擲筊結果（聖筊/笑筊/怒筊）

    Flask->>Model: 儲存擲筊結果
    Model->>DB: INSERT INTO history
    DB-->>Model: 儲存成功
    Model-->>Flask: 確認完成

    Flask-->>Browser: 渲染 result.html（擲筊結果）
    Browser-->>User: 顯示筊杯結果與說明
```

### 2.4 查看歷史紀錄序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 進入歷史紀錄頁面
    Browser->>Flask: GET /history
    Flask->>Model: 查詢所有歷史紀錄
    Model->>DB: SELECT * FROM history ORDER BY date DESC
    DB-->>Model: 回傳紀錄列表
    Model-->>Flask: 回傳紀錄物件列表
    Flask-->>Browser: 渲染 index.html（紀錄列表）
    Browser-->>User: 顯示歷史紀錄列表
```

### 2.5 刪除歷史紀錄序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser->>Flask: POST /history/delete/<id>
    Flask->>Model: 刪除指定紀錄
    Model->>DB: DELETE FROM history WHERE id = ?
    DB-->>Model: 刪除成功
    Model-->>Flask: 確認完成
    Flask-->>Browser: 重導向到 /history
    Browser-->>User: 顯示更新後的紀錄列表
```

### 2.6 捐香油錢序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 進入捐香油錢頁面
    Browser->>Flask: GET /donation
    Flask-->>Browser: 渲染 index.html（捐款頁面）

    User->>Browser: 選擇金額，點擊「捐款」
    Browser->>Flask: POST /donation
    Flask->>Model: 儲存捐款紀錄
    Model->>DB: INSERT INTO donations
    DB-->>Model: 儲存成功
    Model-->>Flask: 確認完成
    Flask-->>Browser: 渲染 thanks.html（感謝頁面）
    Browser-->>User: 顯示感謝動畫與祝福語
```

---

## 3. 功能清單對照表

> 列出系統中每個功能對應的 URL 路徑、HTTP 方法與說明。

### 3.1 首頁與每日運勢（main_bp）

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|----------|-----------|------|
| 首頁 | `/` | GET | 顯示每日運勢 + 算命方式導覽卡片 |

### 3.2 抽籤功能（fortune_bp）

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|----------|-----------|------|
| 抽籤頁面 | `/fortune/draw` | GET | 顯示選擇類別頁面 |
| 執行抽籤 | `/fortune/draw` | POST | 隨機抽籤、儲存結果、顯示籤詩 |

### 3.3 塔羅占卜功能（tarot_bp）

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|----------|-----------|------|
| 選擇主題與牌陣 | `/tarot/select` | GET | 顯示主題與牌陣選擇頁面 |
| 執行占卜 | `/tarot/select` | POST | 隨機抽牌、儲存結果、顯示解讀 |

### 3.4 擲筊功能（bwa_bp）

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|----------|-----------|------|
| 擲筊頁面 | `/bwa/throw` | GET | 顯示輸入問題頁面 |
| 執行擲筊 | `/bwa/throw` | POST | 隨機擲筊、儲存結果、顯示結果 |

### 3.5 歷史紀錄功能（history_bp）

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|----------|-----------|------|
| 歷史紀錄列表 | `/history` | GET | 顯示所有算命紀錄（支援篩選） |
| 刪除紀錄 | `/history/delete/<id>` | POST | 刪除指定的歷史紀錄 |

### 3.6 捐香油錢功能（donation_bp）

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|----------|-----------|------|
| 捐款頁面 | `/donation` | GET | 顯示香油錢捐款頁面 |
| 執行捐款 | `/donation` | POST | 模擬捐款、儲存紀錄、顯示感謝 |

---

> 📌 **下一步：** 流程圖確認無誤後，進入 **階段四：資料庫設計**（使用 `/db-design` skill）。
