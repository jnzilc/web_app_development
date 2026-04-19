"""
History Model — 歷史紀錄資料模型

負責操作 history 資料表，統一管理抽籤、塔羅、擲筊的算命紀錄。
"""

import sqlite3


class History:
    """歷史紀錄資料模型"""

    def __init__(self, db_path):
        """
        初始化 History Model。

        Args:
            db_path (str): SQLite 資料庫檔案路徑
        """
        self.db_path = db_path

    def _get_connection(self):
        """取得資料庫連線，並設定 row_factory 以便用欄位名稱存取資料。"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, type_, category=None, question=None, result_summary='', result_detail=''):
        """
        新增一筆歷史紀錄。

        Args:
            type_ (str): 算命類型（'fortune' / 'tarot' / 'bwa'）
            category (str, optional): 類別或主題
            question (str, optional): 使用者的問題
            result_summary (str): 結果摘要
            result_detail (str): 結果詳細內容（JSON）

        Returns:
            int: 新增的紀錄 ID，失敗回傳 None
        """
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                """
                INSERT INTO history (type, category, question, result_summary, result_detail)
                VALUES (?, ?, ?, ?, ?)
                """,
                (type_, category, question, result_summary, result_detail)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[History.create] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    def get_all(self):
        """
        取得所有歷史紀錄，按時間倒序排列。

        Returns:
            list[dict]: 所有歷史紀錄的列表
        """
        try:
            conn = self._get_connection()
            rows = conn.execute(
                "SELECT * FROM history ORDER BY created_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[History.get_all] 資料庫錯誤: {e}")
            return []
        finally:
            conn.close()

    def get_by_id(self, history_id):
        """
        根據 ID 取得單筆歷史紀錄。

        Returns:
            dict or None: 歷史紀錄資料
        """
        try:
            conn = self._get_connection()
            row = conn.execute(
                "SELECT * FROM history WHERE id = ?", (history_id,)
            ).fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[History.get_by_id] 資料庫錯誤: {e}")
            return None
        finally:
            conn.close()

    def get_by_type(self, type_):
        """
        根據算命類型篩選歷史紀錄。

        Args:
            type_ (str): 算命類型（'fortune' / 'tarot' / 'bwa'）

        Returns:
            list[dict]: 該類型的紀錄列表
        """
        try:
            conn = self._get_connection()
            rows = conn.execute(
                "SELECT * FROM history WHERE type = ? ORDER BY created_at DESC",
                (type_,)
            ).fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[History.get_by_type] 資料庫錯誤: {e}")
            return []
        finally:
            conn.close()

    def delete(self, history_id):
        """
        刪除指定 ID 的歷史紀錄。

        Returns:
            bool: 是否成功刪除
        """
        try:
            conn = self._get_connection()
            cursor = conn.execute(
                "DELETE FROM history WHERE id = ?", (history_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[History.delete] 資料庫錯誤: {e}")
            return False
        finally:
            conn.close()
