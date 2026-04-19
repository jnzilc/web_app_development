"""
History Routes — 歷史紀錄功能路由

Blueprint: history_bp
URL 前綴: /history
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.history import History

history_bp = Blueprint('history', __name__, url_prefix='/history')

TYPE_NAMES = {
    'fortune': '🎋 抽籤',
    'tarot': '🃏 塔羅牌',
    'bwa': '🙏 擲筊'
}


@history_bp.route('/', methods=['GET'])
def index():
    """歷史紀錄列表頁面 — 支援依類型篩選"""
    db_path = current_app.config['DATABASE']
    history_model = History(db_path)

    filter_type = request.args.get('type', '')

    if filter_type and filter_type in TYPE_NAMES:
        records = history_model.get_by_type(filter_type)
    else:
        records = history_model.get_all()
        filter_type = ''

    return render_template('history/index.html',
                           records=records,
                           filter_type=filter_type,
                           type_names=TYPE_NAMES)


@history_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """刪除歷史紀錄"""
    db_path = current_app.config['DATABASE']
    history_model = History(db_path)

    success = history_model.delete(id)
    if success:
        flash('紀錄已成功刪除', 'success')
    else:
        flash('紀錄不存在或刪除失敗', 'error')

    return redirect(url_for('history.index'))
