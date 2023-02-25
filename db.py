from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import get_config

config = get_config()
engine = create_engine(config.sqlalchemy_url)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
