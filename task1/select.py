import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError, DatabaseError

load_dotenv()

def execute_query(sql: str, fetch: bool = True) -> list:
    """Execute a SQL query on PostgreSQL and return results if applicable."""
    try:
        with psycopg2.connect(
            dbname=os.getenv("PG_DB_NAME"),
            user=os.getenv("PG_DB_USER"),
            password=os.getenv("PG_DB_PASSWORD"),
            host=os.getenv("PG_DB_HOST"),
            port=os.getenv("PG_DB_PORT")
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                if fetch:
                    return cur.fetchall()
                conn.commit()
                return []
    except (OperationalError, DatabaseError) as e:
        print(f"Database error: {e}")
        return []

def main():
    queries = {
        "1. Отримати всі завдання для користувача з id = 1": """
            SELECT * FROM tasks WHERE user_id = 1
        """,

        "2. Вибрати завдання зі статусом 'new'": """
            SELECT * FROM tasks
            WHERE status_id = (SELECT id FROM status WHERE name = 'new')
        """,

        "3. Змінити статус завдання з id = 1 на 'in progress'": """
            UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress')
            WHERE id = 1
        """,

        "4. Отримати список користувачів, які не мають жодного завдання": """
            SELECT * FROM users
            WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)
        """,

        "5. Додати нове завдання для користувача з id = 2": """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES ('New generated task', 'Simple description', 1, 2)
        """,

        "6. Отримати всі завдання, які ще не завершено": """
            SELECT * FROM tasks
            WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
        """,

        "7. Видалити завдання з id = 3": """
            DELETE FROM tasks WHERE id = 3
        """,

        "8. Знайти користувачів з електронною поштою '@example.com'": """
            SELECT * FROM users WHERE email LIKE '%@example.com'
        """,

        "9. Оновити ім'я користувача з id = 4 на 'Updated Name'": """
            UPDATE users SET fullname = 'Updated Name' WHERE id = 4
        """,

        "10. Отримати кількість завдань для кожного статусу": """
            SELECT s.name, COUNT(t.id)
            FROM status s
            LEFT JOIN tasks t ON t.status_id = s.id
            GROUP BY s.name
        """,

        "11. Отримати завдання, які призначені користувачам з доменною частиною електронної пошти 'example.com'": """
            SELECT t.*
            FROM tasks t
            JOIN users u ON t.user_id = u.id
            WHERE u.email LIKE '%@example.com'
        """,

        "12. Отримати список завдань, що не мають опису": """
            SELECT * FROM tasks WHERE description IS NULL
        """,

        "13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. Впорядкoванo за ім'ям користувача": """
            SELECT u.fullname, t.title
            FROM users u
            JOIN tasks t ON t.user_id = u.id
            JOIN status s ON t.status_id = s.id
            WHERE s.name = 'in progress'
            ORDER BY u.fullname
        """,

        "14. Отримати користувачів та кількість їхніх завдань": """
            SELECT u.fullname, COUNT(t.id)
            FROM users u
            LEFT JOIN tasks t ON u.id = t.user_id
            GROUP BY u.fullname
        """
    }

    for description, sql in queries.items():
        print(f"\n{description}\n")
        fetch = not sql.strip().upper().startswith(("UPDATE", "INSERT", "DELETE"))
        result = execute_query(sql, fetch=fetch)
        
        if fetch:
            if result:
                for row in result:
                    print(row)
            else:
                print("No results found.")
        else:
            print("Query executed successfully (no results to return).")


if __name__ == "__main__":
    main()