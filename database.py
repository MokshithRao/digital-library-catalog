from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./digital_library.db"


# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)


# Create database session
SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine
)



# Base class for database models
Base = declarative_base()

