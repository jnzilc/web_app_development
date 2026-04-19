"""
應用程式入口點 — 建立並啟動 Flask app
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
