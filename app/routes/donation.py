"""
Donation Routes — 捐香油錢功能路由

Blueprint: donation_bp
URL 前綴: /donation
"""

import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.donation import Donation

donation_bp = Blueprint('donation', __name__, url_prefix='/donation')

BLESSINGS = [
    '願神明保佑你平安順遂、萬事如意！🙏',
    '功德無量！願你心想事成、一切順利！✨',
    '善心有善報，願你福運綿長！🌟',
    '感謝你的虔誠，神明必會庇佑！🏮',
    '積善之家必有餘慶，願你吉祥如意！🎊',
    '一片誠心達天聽，願你所求皆如願！🌺',
]


@donation_bp.route('/', methods=['GET'])
def index():
    """捐香油錢頁面 — 顯示捐款表單與歷史總額"""
    db_path = current_app.config['DATABASE']
    donation_model = Donation(db_path)
    total = donation_model.get_total()

    return render_template('donation/index.html', total=total)


@donation_bp.route('/', methods=['POST'])
def donate():
    """執行捐款 — 驗證金額、儲存紀錄、顯示感謝"""
    amount_str = request.form.get('amount', '').strip()
    message = request.form.get('message', '').strip()

    # 驗證金額
    try:
        amount = int(amount_str)
        if amount <= 0:
            raise ValueError("金額必須為正整數")
    except (ValueError, TypeError):
        flash('請輸入有效的捐款金額（正整數）', 'error')
        return redirect(url_for('donation.index'))

    db_path = current_app.config['DATABASE']
    donation_model = Donation(db_path)
    donation_model.create(amount, message)

    blessing = random.choice(BLESSINGS)

    return render_template('donation/thanks.html',
                           amount=amount,
                           message=message,
                           blessing=blessing)
