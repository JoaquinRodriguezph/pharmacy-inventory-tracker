import os
import psycopg
from psycopg.rows import dict_row


def get_connection():
    """Open a connection to the local pharmacy database."""
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="pharmacy",
        user="postgres",
        password=os.environ.get("PGPASSWORD", "password"),
    )


def get_dict_connection():
    """Same as get_connection, but rows come back as dicts (for the API)."""
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="pharmacy",
        user="postgres",
        password=os.environ.get("PGPASSWORD", "password"),
        row_factory=dict_row,
    )