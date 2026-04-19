"""
Tarot Routes — 塔羅牌占卜功能路由

Blueprint: tarot_bp
URL 前綴: /tarot
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.tarot import Tarot
from app.models.history import History

tarot_bp = Blueprint('tarot', __name__, url_prefix='/tarot')

TOPICS = ['愛情', '事業', '人際', '當日運勢']
SPREADS = {'single': 1, 'three': 3}
SPREAD_NAMES = {'single': '單張牌', 'three': '三張牌（過去/現在/未來）'}
POSITION_LABELS = {0: '過去', 1: '現在', 2: '未來'}


@tarot_bp.route('/select', methods=['GET'])
def select():
    """選擇主題與牌陣頁面"""
    return render_template('tarot/select.html', topics=TOPICS, spreads=SPREAD_NAMES)


@tarot_bp.route('/select', methods=['POST'])
def select_result():
    """執行塔羅占卜 — 隨機抽牌、儲存結果、顯示解讀"""
    topic = request.form.get('topic', '')
    spread = request.form.get('spread', '')

    # 驗證輸入
    if topic not in TOPICS:
        flash('請選擇有效的占卜主題', 'error')
        return redirect(url_for('tarot.select'))

    if spread not in SPREADS:
        flash('請選擇有效的牌陣', 'error')
        return redirect(url_for('tarot.select'))

    db_path = current_app.config['DATABASE']
    tarot_model = Tarot(db_path)
    history_model = History(db_path)

    count = SPREADS[spread]
    cards = tarot_model.get_random(count)

    if not cards:
        flash('目前暫無塔羅牌資料', 'warning')
        return redirect(url_for('tarot.select'))

    # 加入位置標籤（三張牌：過去/現在/未來）
    for i, card in enumerate(cards):
        if spread == 'three':
            card['position'] = POSITION_LABELS.get(i, '')
        else:
            card['position'] = '指引'

    # 儲存到歷史紀錄
    card_names = '、'.join([c['name'] for c in cards])
    result_detail = json.dumps(cards, ensure_ascii=False)
    history_model.create(
        type_='tarot',
        category=topic,
        result_summary=card_names,
        result_detail=result_detail
    )

    return render_template('tarot/result.html',
                           cards=cards,
                           topic=topic,
                           spread_name=SPREAD_NAMES[spread])
