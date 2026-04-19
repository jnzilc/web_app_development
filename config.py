"""
設定檔 — 集中管理 Flask 應用程式設定
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基礎設定"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change')
    DATABASE = os.path.join(BASE_DIR, 'instance', 'database.db')
