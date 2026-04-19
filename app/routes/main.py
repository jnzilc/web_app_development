"""
Main Routes — 首頁與每日運勢路由

Blueprint: main_bp
URL 前綴: /
"""

import random
from datetime import date
from flask import Blueprint, render_template, current_app

main_bp = Blueprint('main', __name__)

# 每日運勢資料
LUCKY_COLORS = ['紅色', '金色', '紫色', '藍色', '綠色', '白色', '橙色', '粉色', '銀色', '黃色']
LUCKY_ITEMS = ['水晶', '紅線', '銅錢', '玉珮', '香包', '護身符', '平安扣', '福袋', '硃砂', '桃木']
DAILY_ADVICE = [
    '今日宜靜不宜動，凡事三思而後行。',
    '貴人運旺盛，把握機會主動出擊。',
    '財運亨通，適合處理財務相關事宜。',
    '感情運上升，多關心身邊的人。',
    '學業運佳，適合閱讀學習新知識。',
    '今日適合沉澱心靈，冥想靜坐有益身心。',
    '事業運旺，勇敢表達想法會有好結果。',
    '健康運需注意，記得多喝水多休息。',
    '人際關係和諧，適合社交聚會。',
    '創意靈感豐富，適合藝術創作。',
    '旅行運佳，外出踏青會有好心情。',
    '今日萬事如意，保持好心情迎接美好的一天。',
]


@main_bp.route('/')
def index():
    """
    首頁 — 顯示每日運勢與功能導覽卡片

    使用日期作為隨機種子，確保同一天內容一致。
    """
    today = date.today()
    seed = int(today.strftime('%Y%m%d'))
    rng = random.Random(seed)

    daily_fortune = {
        'date': today.strftime('%Y 年 %m 月 %d 日'),
        'weekday': ['一', '二', '三', '四', '五', '六', '日'][today.weekday()],
        'lucky_color': rng.choice(LUCKY_COLORS),
        'lucky_number': rng.randint(1, 99),
        'lucky_item': rng.choice(LUCKY_ITEMS),
        'star_rating': rng.randint(3, 5),
        'advice': rng.choice(DAILY_ADVICE),
    }

    return render_template('index.html', daily=daily_fortune)
