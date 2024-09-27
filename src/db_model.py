from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    translations = relationship('Translation', back_populates='user')
    file_translations = relationship('FileTranslation', back_populates='user')


class Translation(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    english_text = Column(String, nullable=False)
    bengali_text = Column(String, nullable=False)
    translated_at = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String)
    user = relationship('User', back_populates='translations')


class FileTranslation(Base):
    __tablename__ = 'file_translations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    input_file = Column(String, nullable=False)
    output_file = Column(String, nullable=False)
    translated_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='file_translations')


# Create the database and tables
def create_database():
    engine = create_engine('sqlite:///db/translation_app.db')
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_database()
    print("Database and tables created successfully.")