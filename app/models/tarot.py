"""
Tarot Model — 塔羅牌資料模型

負責操作 tarots 資料表，提供塔羅牌的 CRUD 方法。
"""

import sqlite3
import random


class Tarot:
    """塔羅牌資料模型"""

    def __init__(self, db_path):
        """
        初始化 Tarot Model。

        Args:
            db_path (str): SQLite 資料庫檔案路徑
        """
        self.db_path = db_path

    def _get_connection(self):
        """取得資料庫連線，並設定 row_factory 以便用欄位名稱存取資料。"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, name, image_url, upright_meaning, reversed_meaning, description):
        """
        新增一張塔羅牌資料。

        Returns:
            int: 新增的塔羅牌 ID，失敗回傳 None
        """
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                """
                INSERT INTO tarots (name, image_url, upright_meaning, reversed_meaning, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, image_url, upright_meaning, reversed_meaning, description)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[Tarot.create] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    def get_all(self):
        """
        取得所有塔羅牌資料。

        Returns:
            list[dict]: 所有塔羅牌的列表
        """
        try:
            conn = self._get_connection()
            rows = conn.execute("SELECT * FROM tarots ORDER BY id").fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[Tarot.get_all] 資料庫錯誤: {e}")
            return []
        finally:
            conn.close()

    def get_by_id(self, tarot_id):
        """
        根據 ID 取得單張塔羅牌。

        Returns:
            dict or None: 塔羅牌資料
        """
        try:
            conn = self._get_connection()
            row = conn.execute(
                "SELECT * FROM tarots WHERE id = ?", (tarot_id,)
            ).fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[Tarot.get_by_id] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    def get_random(self, count=1):
        """
        隨機抽取指定數量的塔羅牌，每張牌隨機決定正位或逆位。

        Args:
            count (int): 要抽取的牌數

        Returns:
            list[dict]: 隨機塔羅牌列表，每張牌包含 is_reversed 欄位
        """
        try:
            conn = self._get_connection()
            rows = conn.execute(
                "SELECT * FROM tarots ORDER BY RANDOM() LIMIT ?", (count,)
            ).fetchall()
            results = []
            for row in rows:
                card = dict(row)
                card['is_reversed'] = random.choice([True, False])
                results.append(card)
            return results
        except sqlite3.Error as e:
            print(f"[Tarot.get_random] 資料庫錯誤: {e}")
            return []
        finally:
            conn.close()

    def delete(self, tarot_id):
        """
        刪除指定 ID 的塔羅牌。

        Returns:
            bool: 是否成功刪除
        """
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                "DELETE FROM tarots WHERE id = ?", (tarot_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[Tarot.delete] 資料庫錯誤: {e}")
            return False
        finally:
            conn.close()

    def count(self):
        """取得塔羅牌總數。"""
        try:
            conn = self._get_connection()
            row = conn.execute("SELECT COUNT(*) as cnt FROM tarots").fetchone()
            return row['cnt']
        except sqlite3.Error as e:
            print(f"[Tarot.count] 資料庫錯誤: {e}")
            return 0
        finally:
            conn.close()
