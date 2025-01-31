from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

# Create SQLite database engine
engine = create_engine('sqlite:///medical_history.db', echo=True)
Base = declarative_base()

class MedicalHistory(Base):
    __tablename__ = 'medical_history'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    symptoms = Column(Text)
    chat_summary = Column(Text)
    ai_recommendations = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)

class MedicalHistoryDB:
    def __init__(self):
        self.Session = Session

    def add_medical_history(self, user_id, symptoms, chat_summary, ai_recommendations):
        session = self.Session()
        try:
            history = MedicalHistory(
                user_id=user_id,
                symptoms=symptoms,
                chat_summary=chat_summary,
                ai_recommendations=ai_recommendations
            )
            session.add(history)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_user_history(self, user_id, limit=5):
        session = self.Session()
        try:
            history = session.query(MedicalHistory)\
                .filter(MedicalHistory.user_id == user_id)\
                .order_by(MedicalHistory.created_at.desc())\
                .limit(limit)\
                .all()
            
            return [(
                h.created_at,
                h.symptoms,
                h.chat_summary,
                h.ai_recommendations
            ) for h in history]
        finally:
            session.close()

    def get_all_history(self):
        session = self.Session()
        try:
            return session.query(MedicalHistory).all()
        finally:
            session.close()