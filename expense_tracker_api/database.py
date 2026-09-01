from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "sqlite:///./expenses.db"


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass