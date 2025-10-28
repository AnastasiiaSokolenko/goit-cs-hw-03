import psycopg2
from faker import Faker
import random

fake = Faker()

conn = psycopg2.connect(
    dbname="task1db",
    user="postgres",
    password="secret_password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Insert statuses
statuses = ['new', 'in progress', 'completed']
cur.executemany("INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING", [(s,) for s in statuses])

# Insert users
for _ in range(10):
    fullname = fake.name()
    email = fake.unique.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

# Insert tasks
cur.execute("SELECT id FROM users")
user_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT id FROM status")
status_ids = [row[0] for row in cur.fetchall()]

for _ in range(30):
    title = fake.sentence(nb_words=4)
    description = fake.text(max_nb_chars=200) if random.random() > 0.2 else None
    user_id = random.choice(user_ids)
    status_id = random.choice(status_ids)
    cur.execute("""
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (%s, %s, %s, %s)
    """, (title, description, status_id, user_id))

conn.commit()
cur.close()
conn.close()