from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

url="sqlite:///./portfolio.db"
engine=create_engine(url,connect_args={"check_same_thread":False})
LocalSession=sessionmaker(bind=engine,autoflush=True)
def get_db():
    db=LocalSession()
    try:
        yield db
    finally:
        db.close()    
