import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read variables from environment
conn = psycopg2.connect(
    dbname=os.getenv("PG_DB_NAME"),
    user=os.getenv("PG_DB_USER"),
    password=os.getenv("PG_DB_PASSWORD"),
    host=os.getenv("PG_DB_HOST"),
    port=os.getenv("PG_DB_PORT")
)
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS status;
""")

cur.execute("""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
""")

cur.execute("""
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
""")

cur.execute("""
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
""")

conn.commit()
cur.close()
conn.close()