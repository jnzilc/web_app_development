"""
Fortune Model — 籤詩資料模型

負責操作 fortunes 資料表，提供籤詩的 CRUD 方法。
"""

import sqlite3


class Fortune:
    """籤詩資料模型"""

    def __init__(self, db_path):
        """
        初始化 Fortune Model。

        Args:
            db_path (str): SQLite 資料庫檔案路徑
        """
        self.db_path = db_path

    def _get_connection(self):
        """取得資料庫連線，並設定 row_factory 以便用欄位名稱存取資料。"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, category, level, poem, interpretation, advice):
        """
        新增一筆籤詩資料。

        Args:
            category (str): 籤詩類別
            level (str): 籤等級
            poem (str): 籤詩原文
            interpretation (str): 白話解釋
            advice (str): 建議與指引

        Returns:
            int: 新增的籤詩 ID，失敗回傳 None
        """
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                """
                INSERT INTO fortunes (category, level, poem, interpretation, advice)
                VALUES (?, ?, ?, ?, ?)
                """,
                (category, level, poem, interpretation, advice)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[Fortune.create] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    def get_all(self):
        """
        取得所有籤詩資料。

        Returns:
            list[dict]: 所有籤詩的列表
        """
        try:
            conn = self._get_connection()
            rows = conn.execute("SELECT * FROM fortunes ORDER BY id").fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[Fortune.get_all] 資料庫錯誤: {e}")
            return []
        finally:
            conn.close()

    def get_by_id(self, fortune_id):
        """
        根據 ID 取得單筆籤詩。

        Args:
            fortune_id (int): 籤詩 ID

        Returns:
            dict or None: 籤詩資料
        """
        try:
            conn = self._get_connection()
            row = conn.execute(
                "SELECT * FROM fortunes WHERE id = ?", (fortune_id,)
            ).fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[Fortune.get_by_id] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    def get_random_by_category(self, category):
        """
        根據類別隨機抽取一支籤詩。

        Args:
            category (str): 籤詩類別

        Returns:
            dict or None: 隨機籤詩資料
        """
        try:
            conn = self._get_connection()
            row = conn.execute(
                "SELECT * FROM fortunes WHERE category = ? ORDER BY RANDOM() LIMIT 1",
                (category,)
            ).fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[Fortune.get_random_by_category] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    def delete(self, fortune_id):
        """
        刪除指定 ID 的籤詩。

        Args:
            fortune_id (int): 籤詩 ID

        Returns:
            bool: 是否成功刪除
        """
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                "DELETE FROM fortunes WHERE id = ?", (fortune_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[Fortune.delete] 資料庫錯誤: {e}")
            return False
        finally:
            conn.close()

    def count(self):
        """
        取得籤詩總數。

        Returns:
            int: 籤詩總數
        """
        try:
            conn = self._get_connection()
            row = conn.execute("SELECT COUNT(*) as cnt FROM fortunes").fetchone()
            return row['cnt']
        except sqlite3.Error as e:
            print(f"[Fortune.count] 資料庫錯誤: {e}")
            return 0
        finally:
            conn.close()
