from contextlib import contextmanager

from ehelply_bootstrapper.utils.state import State


# Dependency
def get_db():
    db = State.mysql.SessionLocal()
    try:
        State.logger.warning("Due to the issue described in the link, I recommend you switch from using Depends(get_db) in your endpoint parameters to using The DbSession context manager. `with DebSession() as db:` https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/104 ")
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def DbSession():
    db = State.mysql.SessionLocal()
    try:
        yield db
    except:
        # if we fail somehow rollback the connection
        # warnings.warn("We somehow failed in a DB operation and auto-rollbacking...")
        db.rollback()
        raise
    finally:
        db.close()
