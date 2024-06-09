import threading
import sqlite3
from sqlite3 import Error


class DataService:
    """Класс для работы с данными пользователей"""

    @staticmethod
    def create_connection(path_to_database):
        connection = None
        try:
            connection = sqlite3.connect(path_to_database, check_same_thread=False)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    path_to_database = '../data/twitch_data.sqlite'
    connection = create_connection('../data/twitch_data.sqlite')
    cursor = connection.cursor()

    @staticmethod
    def execute_query_init(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    @staticmethod
    def create_streamers_table(connection):
        create_streamers_query = """
        CREATE TABLE IF NOT EXISTS streamers (
          streamer_id INTEGER PRIMARY KEY AUTOINCREMENT,
          login TEXT NOT NULL,
          status BOOLEAN NOT NULL DEFAULT FALSE
        );
        """
        DataService.execute_query_init(connection, create_streamers_query)

    @staticmethod
    def create_users_table(connection):
        create_users_query = """
        CREATE TABLE IF NOT EXISTS users (
          user_id INTEGER PRIMARY KEY AUTOINCREMENT,
          login TEXT NOT NULL
        );
        """
        DataService.execute_query_init(connection, create_users_query)

    @staticmethod
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
        DataService.execute_query_init(connection, create_users_to_streamers_link_query)

    def __init__(self, path_to_streamers_file, path_to_users_file):
        DataService.create_streamers_table(self.connection)
        DataService.create_users_table(self.connection)
        DataService.create_users_to_streamers_link_table(self.connection)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query):
        result = None
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
        return None

    def get_streamer_status(self, streamer):
        get_streamer_query = f"""
            SELECT status 
            from streamers
            where login = '{streamer}'
            limit 1
            """
        result = self.execute_read_query(get_streamer_query)
        if result is None or len(result) == 0:
            return None
        if result[0][0]:
            return True
        return False

    def add_streamer(self, streamer):
        insert_streamer_query = f"""
            INSERT INTO streamers (login)
            VALUES
              ('{streamer}')
        """
        self.execute_query(insert_streamer_query)

    def get_streamers(self):
        get_streamers_query = "SELECT login, status from streamers"
        result_query = self.execute_read_query(get_streamers_query)
        result = {}
        for currentStreamer in result_query:
            if currentStreamer[1] == 0:
                result[currentStreamer[0]] = False
            else:
                result[currentStreamer[0]] = True
        return result

    def get_streamer_id(self, streamer):
        get_streamer_id_query = f"""
            SELECT streamer_id 
            from streamers
            where login = '{streamer}'
            limit 1
            """
        result = self.execute_read_query(get_streamer_id_query)
        if result is None or len(result) == 0:
            return None
        return result[0][0]

    def add_user(self, user):
        insert_streamer_query = f"""
            INSERT INTO users (login)
            VALUES
              ('{user}')
        """
        self.execute_query(insert_streamer_query)

    def get_user_id(self, user):
        get_user_id_query = f"""
            SELECT user_id 
            from users
            where login = '{user}'
            limit 1
            """
        result = self.execute_read_query(get_user_id_query)
        if result is None or len(result) == 0:
            return None
        return result[0][0]

    def add_user_for_streamer(self, streamer, user):
        streamer_id = self.get_streamer_id(streamer)
        if streamer_id is None:
            self.add_streamer(streamer)
            streamer_id = self.get_streamer_id(streamer)
        user_id = self.get_user_id(user)
        if user_id is None:
            self.add_user(user)
            user_id = self.get_user_id(user)
        insert_users_to_streamers_link_query = f"""
            INSERT INTO users_to_streamers_link (user_id, streamer_id)
            VALUES
              ({user_id}, {streamer_id})
        """
        self.execute_query(insert_users_to_streamers_link_query)

    def get_users_for_streamer(self, streamer):
        streamer_id = self.get_streamer_id(streamer)
        if streamer_id is None:
            return None
        get_users_to_streamers_link_query = f"""
            with pre as (
                select user_id
                from users_to_streamers_link
                where streamer_id = {streamer_id}
            )
            select users.login
            from pre
            join users on
                pre.user_id = users.user_id
        """
        result_query = self.execute_read_query(get_users_to_streamers_link_query)
        result = []
        for current_user in result_query:
            result.append(current_user[0])
        return result

    def update_streamers_status(self, change_dict):
        for current_streamer in change_dict:
            update_streamer_status = f"""
                UPDATE streamers
                SET status = {change_dict.get(current_streamer)}
                WHERE login = '{current_streamer}'
            """
            self.execute_query(update_streamer_status)

    def drop_table(self, table_name):
        drop_table_query = """ DROP table """ + table_name
        self.execute_query(drop_table_query)
