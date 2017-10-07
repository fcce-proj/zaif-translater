from sqlalchemy import Column, Integer, Text

from .meta import Base


class Phrase(Base):
    __tablename__ = 'phrases'
    id = Column(Integer, primary_key=True)
    key_lang = Column(Text, nullable=False)
    ja = Column(Text, nullable=False)
    en = Column(Text, nullable=False)
    zh = Column(Text, nullable=False)