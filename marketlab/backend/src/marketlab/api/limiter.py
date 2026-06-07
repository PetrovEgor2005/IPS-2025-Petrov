"""
Slowapi ограничивает количество запросов с одного IP(в другом блоке установлено значение 20 запросов в минуту)
"""

from __future__ import annotations
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
