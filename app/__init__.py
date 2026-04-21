"""
Flask 應用程式工廠 — 初始化 Flask app、資料庫、註冊 Blueprint
"""

import os
import sqlite3
from flask import Flask, g, current_app
from config import Config

def get_db():
    """取得資料庫連線（每次請求共用同一個連線）"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE']
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """關閉資料庫連線"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    """根據 schema.sql 初始化資料庫"""
    db_path = app.config['DATABASE']

    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    # 取得專案根目錄 (app 資料夾的上一層)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(project_root, 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def create_app():
    """
    Flask 應用程式工廠函式

    Returns:
        Flask: 配置完成的 Flask 應用程式實例
    """
    app = Flask(__name__,
                instance_relative_config=False)

    app.config.from_object(Config)

    # 初始化資料庫
    init_db(app)

    # 註冊資料庫清除函式
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db(exception)

    # 讓所有模板與路由可以取得 db_path
    @app.before_request
    def before_request():
        g._app_config = app.config

    # 註冊 Blueprint
    from app.routes import main_bp, fortune_bp, tarot_bp, bwa_bp, history_bp, donation_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(fortune_bp)
    app.register_blueprint(tarot_bp)
    app.register_blueprint(bwa_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(donation_bp)

    return app
