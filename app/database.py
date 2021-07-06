import os

from psycopg2 import pool

DB_POOL = None


def get_pool():
    global DB_POOL
    if DB_POOL is None:
        DB_POOL = pool.ThreadedConnectionPool(minconn=2,
                                              maxconn=4,
                                              user=os.getenv("POSTGRES_USERNAME"),
                                              password=os.getenv("POSTGRES_PASSWORD"),
                                              database=os.getenv("POSTGRES_DATABASE"),
                                              host=os.getenv("POSTGRES_HOST"))
    return DB_POOL


def get_connection():
    return get_pool().getconn()


def release_connection(conn):
    DB_POOL.putconn(conn)
