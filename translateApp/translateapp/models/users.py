from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    TIMESTAMP,
)

import datetime
import sqlalchemy.ext.declarative
Base = sqlalchemy.ext.declarative.declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password_hash = Column(Text, nullable=False)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False


class Phrase(Base):
    __tablename__ = 'phrase'
    id = Column(Integer, primary_key=True)
    key_lang = Column(Text, nullable=False)
    ja = Column(Text, nullable=False)
    en = Column(Text, nullable=False)
    zh = Column(Text, nullable=False)
    # add_timestamp = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())
    # update_timestamp = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())

url = 'postgresql+pypostgresql://pyramid_user:password@localhost/project_db'
engine = sqlalchemy.create_engine(url, echo=True)
# スキーマ作成
Base.metadata.create_all(engine)
