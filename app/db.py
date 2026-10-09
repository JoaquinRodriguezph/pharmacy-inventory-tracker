import os
import psycopg


def get_connection():
    """Open a connection to the local pharmacy database."""
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="pharmacy",
        user="postgres",
        password=os.environ.get("PGPASSWORD", "password"),
    )