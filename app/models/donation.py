"""
Donation Model — 捐款紀錄資料模型

負責操作 donations 資料表，管理香油錢捐款紀錄。
"""

import sqlite3


class Donation:
    """捐款紀錄資料模型"""

    def __init__(self, db_path):
        """
        初始化 Donation Model。

        Args:
            db_path (str): SQLite 資料庫檔案路徑
        """
        self.db_path = db_path

    def _get_connection(self):
        """取得資料庫連線，並設定 row_factory 以便用欄位名稱存取資料。"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, amount, message=''):
        """
        新增一筆捐款紀錄。

        Args:
            amount (int): 捐款金額（元）
            message (str, optional): 祈願留言

        Returns:
            int: 新增的捐款紀錄 ID，失敗回傳 None
        """
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                "INSERT INTO donations (amount, message) VALUES (?, ?)",
                (amount, message)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[Donation.create] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    def get_all(self):
        """
        取得所有捐款紀錄，按時間倒序排列。

        Returns:
            list[dict]: 所有捐款紀錄的列表
        """
        try:
            conn = self._get_connection()
            rows = conn.execute(
                "SELECT * FROM donations ORDER BY created_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[Donation.get_all] 資料庫錯誤: {e}")
            return []
        finally:
            conn.close()

    def get_total(self):
        """
        取得捐款總金額。

        Returns:
            int: 總捐款金額
        """
        try:
            conn = self._get_connection()
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM donations"
            ).fetchone()
            return row['total']
        except sqlite3.Error as e:
            print(f"[Donation.get_total] 資料庫錯誤: {e}")
            return 0
        finally:
            conn.close()

    def delete(self, donation_id):
        """
        刪除指定 ID 的捐款紀錄。

        Returns:
            bool: 是否成功刪除
        """
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                "DELETE FROM donations WHERE id = ?", (donation_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[Donation.delete] 資料庫錯誤: {e}")
            return False
        finally:
            conn.close()
