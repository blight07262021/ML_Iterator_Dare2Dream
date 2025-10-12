#### **`backend/app/database.py`**

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# !!! IMPORTANT !!!
# UPDATE THIS LINE WITH YOUR MYSQL DATABASE CREDENTIALS
# Format: "mysql+pymysql://<user>:<password>@<host>/<dbname>"

# Database credentials
DB_USER = "root"
DB_PASS = "1234567890"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "market_research"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Optional quick connection check
try:
    conn = engine.connect()
    print("✅ Database connection OK")
    conn.close()
except Exception as e:
    print("❌ Database connection error:", e)

