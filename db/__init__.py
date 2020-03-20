import sqlalchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from settings import DATABASE_URI
from logger import log


engine = sqlalchemy.create_engine(DATABASE_URI)
session_maker = sessionmaker(bind=engine)


def safe_commit(session):
    try:
        session.commit()
    except SQLAlchemyError:
        log.exception("DB commiting failed")
        return
    except Exception:
        log.error("Something unexpected happened")
        raise
