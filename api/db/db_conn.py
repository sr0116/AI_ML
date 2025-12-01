from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
#  데이터 베이스 연동
# 로컬용
DB_URL = "postgresql+psycopg2://kinitto:kinitto@localhost:5432/mydb"
# jdbc:postgresql://43.200.237.241:5437/mydb

# DB_URL = "postgresql+psycopg2://kinitto:kinitto@43.200.237.241:5437/mydb"
engine: Engine = create_engine(DB_URL, echo=False, future=True)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)