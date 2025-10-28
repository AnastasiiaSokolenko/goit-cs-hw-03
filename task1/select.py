import psycopg2

conn = psycopg2.connect(
    dbname="task1db",
    user="postgres",
    password="secret_password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

print("\n1. Отримати всі завдання для користувача з id = 1")
cur.execute("SELECT * FROM tasks WHERE user_id = 1")
print(cur.fetchall())

print("\n2. Вибрати завдання зі статусом 'new'")
cur.execute("""
SELECT * FROM tasks
WHERE status_id = (SELECT id FROM status WHERE name = 'new')
""")
print(cur.fetchall())

print("\n3. Змінити статус завдання з id = 1 на 'in progress'")
cur.execute("""
UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1
""")
conn.commit()

print("\n4. Отримати список користувачів, які не мають жодного завдання")
cur.execute("""
SELECT * FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)
""")
print(cur.fetchall())

print("\n5. Додати нове завдання для користувача з id = 2")
cur.execute("""
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New generated task', 'Simple description', 1, 2)
""")
conn.commit()

print("\n6. Отримати всі завдання, які ще не завершено")
cur.execute("""
SELECT * FROM tasks
WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
""")
print(cur.fetchall())

print("\n7. Видалити завдання з id = 3")
cur.execute("DELETE FROM tasks WHERE id = 3")
conn.commit()

print("\n8. Знайти користувачів з електронною поштою '@example.com'")
cur.execute("SELECT * FROM users WHERE email LIKE '%@example.com'")
print(cur.fetchall())

print("\n9. Оновити ім'я користувача з id = 4 на 'Updated Name'")
cur.execute("UPDATE users SET fullname = 'Updated Name' WHERE id = 4")
conn.commit()

print("\n10. Отримати кількість завдань для кожного статусу")
cur.execute("""
SELECT s.name, COUNT(t.id) FROM status s
LEFT JOIN tasks t ON t.status_id = s.id
GROUP BY s.name
""")
print(cur.fetchall())

print("\n11. Отримати завдання, які призначені користувачам з доменною частиною електронної пошти 'example.com'")
cur.execute("""
SELECT t.* FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com'
""")
print(cur.fetchall())

print("\n12. Отримати список завдань, що не мають опису")
cur.execute("SELECT * FROM tasks WHERE description IS NULL")
print(cur.fetchall())

print("\n13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'")
cur.execute("""
SELECT u.fullname, t.title FROM users u
JOIN tasks t ON t.user_id = u.id
JOIN status s ON t.status_id = s.id
WHERE s.name = 'in progress'
""")
print(cur.fetchall())

print("\n14. Отримати користувачів та кількість їхніх завдань")
cur.execute("""
SELECT u.fullname, COUNT(t.id) FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.fullname
""")
print(cur.fetchall())

cur.close()
conn.close()