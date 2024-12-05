from sqlalchemy import Column, CHAR, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(DateTime(timezone=True), index=True)  # Primary key
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    from_country = Column(CHAR(3), nullable=False)
    to_country = Column(CHAR(3), nullable=False)

