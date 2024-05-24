import sqlite3
import os


class MessagesDatabase:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.__create_database()
        
    
    # Создание БД
    def __create_database(self) -> None:
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'x') as f:
                pass
                
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        CREATE TABLE IF NOT EXISTS users_data(
          id INTEGER PRIMARY KEY,
          user_id INTEGER,
          message TEXT,
          tokens INTEGER  
        );
        '''
        
        cur.execute(sql_query)
        conn.commit()
        conn.close()
        
    
    # Вставка строки
    def insert_row(self, user_id: int, message: str, tokens: int) -> None:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        INSERT INTO users_data(user_id, message, tokens) VALUES(?, ?, ?);
        '''
        
        cur.execute(sql_query, (user_id, message, tokens, ))
        
        conn.commit()
        conn.close()
        
    
    # Подсчитывает все токены юзера по его Id
    def collect_all_tokens(self, user_id) -> int:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        SELECT SUM(tokens) FROM users_data WHERE user_id = ?;
        '''
        
        result = cur.execute(sql_query, (user_id, )).fetchone()
        
        return result[0]

    
    # Подсчитывает кол-во юзеров исключая user_id (Надо для ограничения юзеров на проект)
    def count_all_users(self, user_id) -> int:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        SELECT DISTINCT user_id FROM users_data WHERE user_id <> ?;
        '''
        
        result = cur.execute(sql_query, (user_id, )).fetchall()
        
        return len(result)


class UsersDatabase:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.__create_database()
        
    
    # Создание БД
    def __create_database(self) -> None:
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'x') as f:
                pass
                
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        CREATE TABLE IF NOT EXISTS users_data(
            user_id INTEGER PRIMARY KEY,
            user_theme TEXT
        );
        '''
        
        cur.execute(sql_query)
        conn.commit()
        conn.close()
    
    
    def get_user_theme(self, user_id: int) -> str:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        SELECT user_theme FROM users_data WHERE user_id = ?;
        '''
        
        result = cur.execute(sql_query, (user_id, )).fetchone()
        
        conn.close()
        return result[0]
    
    
    def set_user_theme(self, user_id: int, theme: str) -> None:
        if not self.is_user_registered(user_id):
            self.register_user(user_id)
        
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        UPDATE users_data SET user_theme = ? WHERE user_id = ?;
        '''
        
        cur.execute(sql_query, (theme, user_id, ))
        
        conn.commit()
        conn.close()
        
    
    def is_user_registered(self, user_id: int) -> None:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        SELECT * FROM users_data WHERE user_id = ?;
        '''
        
        result = cur.execute(sql_query, (user_id, )).fetchone()
        
        conn.close()
        return not result is None
    
    
    def register_user(self, user_id: int) -> None:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        INSERT INTO users_data(user_id, user_theme) VALUES(?, '');
        '''
        
        cur.execute(sql_query, (user_id, ))
        
        conn.commit()
        conn.close()
        
    
    def count_users(self, user_id: int) -> None:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()
        
        sql_query = '''
        SELECT user_id FROM users_data WHERE user_id <> ?;
        '''
        
        result = cur.execute(sql_query, (user_id, )).fetchall()
        
        conn.close()
        return len(result)