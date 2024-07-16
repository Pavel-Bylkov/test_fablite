import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Конфигурация базы данных
DB_NAME = "test_fablite"
DB_USER = "test_user"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
ADMIN_USER = "postgres"
ADMIN_PASSWORD = "postgres"

# Подключение к PostgreSQL как администратор
conn = psycopg2.connect(dbname="postgres", user=ADMIN_USER, password=ADMIN_PASSWORD, host=DB_HOST, port=DB_PORT)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# Создание пользователя
try:
    cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';")
    print(f"User {DB_USER} created successfully.")
except psycopg2.errors.DuplicateObject:
    print(f"User {DB_USER} already exists.")

# Создание базы данных
try:
    cursor.execute(f"CREATE DATABASE {DB_NAME};")
    print(f"Database {DB_NAME} created successfully.")
except psycopg2.errors.DuplicateDatabase:
    print(f"Database {DB_NAME} already exists.")

# Предоставление прав пользователю на базу данных
cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};")
print(f"Granted all privileges on database {DB_NAME} to user {DB_USER}.")

# Подключение к новой базе данных для предоставления прав на схему public
conn.close()
conn = psycopg2.connect(dbname=DB_NAME, user=ADMIN_USER, password=ADMIN_PASSWORD, host=DB_HOST, port=DB_PORT)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# Предоставление прав на схему public
cursor.execute(f"GRANT ALL PRIVILEGES ON SCHEMA public TO {DB_USER};")
print(f"Granted all privileges on schema public to user {DB_USER}.")

# Закрытие соединения
cursor.close()
conn.close()