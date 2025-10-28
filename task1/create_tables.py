import psycopg2

conn = psycopg2.connect(
    dbname="task1db",
    user="postgres",
    password="secret_password",
    host="localhost",
    port="5432"
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