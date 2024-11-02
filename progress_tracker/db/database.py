#database connection using SQLALCHEMY

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Change this to 'mysql://user:password@localhost/progress_tracker' for MySQL
DATABASE_URL = "sqlite:///progress_tracker/progress_tracker/progress_tracker.db"

# Create an engine and a session
engine = create_engine(DATABASE_URL)

Base = declarative_base()

# Create a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import your models and create the tables in the database
def init_db():
    # Import your models here to ensure they are registered with the Base
    from tracker_app.models import User, Admin, Book, Tracker
    Base.metadata.create_all(bind=engine)