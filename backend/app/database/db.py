import oracledb
from app.config import get_settings
from app.logger import get_logger
from contextlib import contextmanager

logger = get_logger("database")
settings = get_settings()


try:
    oracledb.init_oracle_client(lib_dir=settings.oracle_client_lib_dir)
    logger.info("Oracle client initialized successfully")
except Exception as e:
    logger.warning(f"Oracle client initialization warning: {e}")


def get_connection():
    
    try:
        dsn = f"{settings.oracle_host}:{settings.oracle_port}/{settings.oracle_service}"
        conn = oracledb.connect(
            user=settings.oracle_user,
            password=settings.oracle_password,
            dsn=dsn
        )
        logger.debug(f"Database connection established to {dsn}")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


@contextmanager
def get_db_context():
    
    conn = None
    try:
        conn = get_connection()
        yield conn
        conn.commit()
        logger.debug("Transaction committed successfully")
    except Exception as e:
        if conn:
            conn.rollback()
            logger.warning(f"Transaction rolled back due to error: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.debug("Database connection closed")


logger.info("Oracle database module initialized")