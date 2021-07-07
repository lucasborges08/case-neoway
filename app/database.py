import os
from contextlib import contextmanager
from psycopg2 import pool
from psycopg2.extras import DictCursor

DB_POOL = None


def get_pool():
    global DB_POOL
    if DB_POOL is None:
        DB_POOL = pool.ThreadedConnectionPool(minconn=4,
                                              maxconn=10,
                                              user=os.getenv("POSTGRES_USERNAME"),
                                              password=os.getenv("POSTGRES_PASSWORD"),
                                              database=os.getenv("POSTGRES_DATABASE"),
                                              host=os.getenv("POSTGRES_HOST"))
    return DB_POOL


@contextmanager
def get_connection():
    db_pool = get_pool()
    conn = db_pool.getconn()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        yield conn, cursor
        conn.commit()
    except Exception as error:
        conn.rollback()
        raise error
    finally:
        cursor.close()
        db_pool.putconn(conn)


def release_connection(conn):
    DB_POOL.putconn(conn)
