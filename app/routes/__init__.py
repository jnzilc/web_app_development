# app/routes/__init__.py
# 路由層初始化模組

from .main import main_bp
from .fortune import fortune_bp
from .tarot import tarot_bp
from .bwa import bwa_bp
from .history import history_bp
from .donation import donation_bp

__all__ = ['main_bp', 'fortune_bp', 'tarot_bp', 'bwa_bp', 'history_bp', 'donation_bp']
