"""
Bwa Routes — 擲筊功能路由

Blueprint: bwa_bp
URL 前綴: /bwa
"""

import json
import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.history import History

bwa_bp = Blueprint('bwa', __name__, url_prefix='/bwa')

# 擲筊結果定義
BWA_RESULTS = {
    'holy': {
        'name': '聖筊',
        'emoji': '✅',
        'description': '一正一反，表示神明同意、認可你的請求。',
        'advice': '你所問之事得到了神明的肯定，可以放心前行。'
    },
    'laugh': {
        'name': '笑筊',
        'emoji': '😄',
        'description': '兩面朝上（正面），表示神明在笑，意思不明確。',
        'advice': '神明似乎覺得你的問題有趣，建議重新整理思緒後再問一次。'
    },
    'angry': {
        'name': '怒筊',
        'emoji': '❌',
        'description': '兩面朝下（反面），表示神明不同意。',
        'advice': '此事目前不宜，建議換個方式或時機再做打算。'
    }
}


@bwa_bp.route('/throw', methods=['GET'])
def throw():
    """擲筊頁面 — 顯示輸入問題頁面"""
    return render_template('bwa/throw.html')


@bwa_bp.route('/throw', methods=['POST'])
def throw_result():
    """執行擲筊 — 隨機擲筊、儲存結果、顯示結果"""
    question = request.form.get('question', '').strip()

    if not question:
        flash('請輸入你想詢問的問題', 'error')
        return redirect(url_for('bwa.throw'))

    # 隨機產生結果
    result_key = random.choice(['holy', 'laugh', 'angry'])
    result = BWA_RESULTS[result_key]

    # 儲存到歷史紀錄
    db_path = current_app.config['DATABASE']
    history_model = History(db_path)

    result_detail = json.dumps({
        'result_key': result_key,
        'name': result['name'],
        'description': result['description'],
        'advice': result['advice']
    }, ensure_ascii=False)

    history_model.create(
        type_='bwa',
        question=question,
        result_summary=result['name'],
        result_detail=result_detail
    )

    return render_template('bwa/result.html', result=result, question=question)
