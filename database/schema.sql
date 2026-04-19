-- ============================================
-- 線上算命系統 — SQLite 資料庫 Schema
-- 版本：v1.0
-- 建立日期：2026-04-19
-- ============================================

-- 籤詩資料表：儲存所有可供抽取的籤詩內容
CREATE TABLE IF NOT EXISTS fortunes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,                                      -- 類別：綜合運勢、感情、事業、學業、財運、健康
    level TEXT NOT NULL,                                         -- 等級：上上籤、上籤、中籤、下籤、下下籤
    poem TEXT NOT NULL,                                          -- 籤詩原文
    interpretation TEXT NOT NULL,                                -- 白話解釋
    advice TEXT NOT NULL,                                        -- 建議與指引
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))  -- 建立時間
);

-- 塔羅牌資料表：儲存所有塔羅牌的牌面資訊
CREATE TABLE IF NOT EXISTS tarots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                                          -- 牌名（如：愚者、魔術師）
    image_url TEXT NOT NULL,                                     -- 牌面圖片路徑
    upright_meaning TEXT NOT NULL,                               -- 正位含義
    reversed_meaning TEXT NOT NULL,                              -- 逆位含義
    description TEXT NOT NULL,                                   -- 牌面描述與象徵意義
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))  -- 建立時間
);

-- 歷史紀錄資料表：統一儲存所有算命類型的結果紀錄
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK (type IN ('fortune', 'tarot', 'bwa')),  -- 算命類型
    category TEXT,                                                    -- 類別或主題（擲筊可為空）
    question TEXT,                                                    -- 使用者的問題（擲筊使用）
    result_summary TEXT NOT NULL,                                     -- 結果摘要
    result_detail TEXT NOT NULL,                                      -- 結果詳細內容（JSON）
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))   -- 建立時間
);

-- 捐款紀錄資料表：記錄每筆模擬香油錢捐款
CREATE TABLE IF NOT EXISTS donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER NOT NULL CHECK (amount > 0),                      -- 捐款金額（元）
    message TEXT DEFAULT '',                                         -- 祈願留言
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))   -- 建立時間
);

-- ============================================
-- 索引：加速常用查詢
-- ============================================

CREATE INDEX IF NOT EXISTS idx_history_type ON history (type);
CREATE INDEX IF NOT EXISTS idx_history_created_at ON history (created_at);
CREATE INDEX IF NOT EXISTS idx_fortunes_category ON fortunes (category);
