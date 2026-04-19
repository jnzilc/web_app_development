# app/models/__init__.py
# Model 層初始化模組

from .fortune import Fortune
from .tarot import Tarot
from .history import History
from .donation import Donation

__all__ = ['Fortune', 'Tarot', 'History', 'Donation']
