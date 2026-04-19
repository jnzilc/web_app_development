"""
Fortune Routes — 抽籤（求籤）功能路由

Blueprint: fortune_bp
URL 前綴: /fortune
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.fortune import Fortune
from app.models.history import History

fortune_bp = Blueprint('fortune', __name__, url_prefix='/fortune')

CATEGORIES = ['綜合運勢', '感情', '事業', '學業', '財運', '健康']


@fortune_bp.route('/draw', methods=['GET'])
def draw():
    """抽籤頁面 — 顯示選擇類別頁面"""
    return render_template('fortune/draw.html', categories=CATEGORIES)


@fortune_bp.route('/draw', methods=['POST'])
def draw_result():
    """執行抽籤 — 隨機抽籤、儲存結果、顯示籤詩"""
    category = request.form.get('category', '')

    # 驗證類別
    if category not in CATEGORIES:
        flash('請選擇有效的求籤類別', 'error')
        return redirect(url_for('fortune.draw'))

    db_path = current_app.config['DATABASE']
    fortune_model = Fortune(db_path)
    history_model = History(db_path)

    # 隨機抽取一支籤
    fortune = fortune_model.get_random_by_category(category)

    if not fortune:
        flash('該類別目前暫無籤詩，請選擇其他類別', 'warning')
        return redirect(url_for('fortune.draw'))

    # 儲存到歷史紀錄
    result_detail = json.dumps(fortune, ensure_ascii=False)
    history_model.create(
        type_='fortune',
        category=category,
        result_summary=fortune['level'],
        result_detail=result_detail
    )

    return render_template('fortune/result.html', fortune=fortune, category=category)
