import psycopg2


DATABASE = 'todos'
USER = 'postgres'
PASSWORD = 'password'
HOST = 'localhost'
PORT = '5433' 


conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
conn.autocommit = True


cursor = conn.cursor()


sql = f"CREATE DATABASE {DATABASE}"
cursor.execute(sql)

print("База данных успешно создана!")

# Закрытие соединения
cursor.close()
conn.close()
