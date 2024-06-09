import sqlite3
import string
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        result = cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def create_streamers_table(connection):
    create_streamers_query = """
    CREATE TABLE IF NOT EXISTS streamers (
      streamer_id INTEGER PRIMARY KEY AUTOINCREMENT,
      login TEXT NOT NULL,
      status BOOLEAN NOT NULL DEFAULT FALSE
    );
    """
    execute_query(connection, create_streamers_query)

def create_users_table(connection):
    create_users_query = """
    CREATE TABLE IF NOT EXISTS users (
      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
      login TEXT NOT NULL
    );
    """
    execute_query(connection, create_users_query)

def create_users_to_streamers_link_table(connection):
    create_users_to_streamers_link_query = """
    CREATE TABLE IF NOT EXISTS users_to_streamers_link (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      streamer_id INTEGER,
      FOREIGN KEY (user_id) REFERENCES users (user_id) 
      FOREIGN KEY (streamer_id) REFERENCES streamers (streamer_id)
    );
    """
    execute_query(connection, create_users_to_streamers_link_query)

def insert_user(connection, login):
    insert_user_query = f"""
        INSERT INTO users (login)
        VALUES
          ('{login}')
    """
    return execute_query(connection, insert_user_query)


def insert_streamer(connection, login):
    insert_streamer_query = f"""
        INSERT INTO streamers (login)
        VALUES
          ('{login}')
    """
    result = execute_query(connection, insert_streamer_query)
    print(result)

def drop_table(connection, table_name):
    drop_table_query = """ DROP table """ + table_name
    execute_query(connection, drop_table_query)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def get_all_strimers(connection):
    get_strimers_query = "SELECT login, status from streamers"
    result = execute_read_query(connection, get_strimers_query)
    return result

def get_streamer(connection, login):
    get_strimer_query = f"""
        SELECT status 
        from streamers
        where login = '{login}'
        limit 1
        """
    result = execute_read_query(connection, get_strimer_query)
    if result is None:
        return None
    if result[0][0]:
        return True
    return False

# def update_strimers(connection, values_dict):
#     for streamers

connection = create_connection('../data/twitch_data.sqlite')
drop_table(connection, 'streamers')
drop_table(connection, 'users')
drop_table(connection, 'users_to_streamers_link')
# create_streamers_table(connection)
# create_users_table(connection)
# create_users_to_streamers_link_table(connection)
# insert_streamer(connection, 'aaa')
# drop_table(connection, 'users')
# create_users_table(connection)
# create_users_to_streamers_link_table(connection)
# insert_user(connection, 'aaa')
# print(get_streamer(connection, 'aaa'))
# print(get_all_strimers(connection))