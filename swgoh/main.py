"""
Здесь будет тело основной программы
"""

from sqlalchemy import create_engine
engine = create_engine('sqlite:///swgoh.db', echo=True)
