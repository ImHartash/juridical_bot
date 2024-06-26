import sqlite3
import logging
from juridical_bot.bot_dir.config import feedback_db, user_db, message_db, LOGS


logging.basicConfig(
    filename=LOGS,
    level=logging.INFO,
    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s",
    filemode="w",
)


class MessagesDatabase:
    def __init__(self) -> None:
        self.__create_database()

    # Создание БД
    def __create_database(self) -> None:
        self.file_name = message_db
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        CREATE TABLE IF NOT EXISTS messages_data(
          id INTEGER PRIMARY KEY,
          user_id INTEGER,
          message TEXT,
          role TEXT,
          tokens INTEGER  
        );
        """

        cur.execute(sql_query)
        conn.commit()
        conn.close()

    # Вставка строки
    def insert_row(self, user_id: int, message: str, tokens: int, role: str) -> None:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        INSERT INTO messages_data(user_id, message, role, tokens) VALUES(?, ?, ?, ?);
        """

        cur.execute(
            sql_query,
            (
                user_id,
                message,
                role,
                tokens,
            ),
        )

        conn.commit()
        conn.close()

    # Подсчитывает все токены юзера по его Id
    def count_all_tokens(self, user_id) -> int:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        SELECT SUM(tokens) FROM messages_data WHERE user_id = ?;
        """

        result = cur.execute(sql_query, (user_id,)).fetchone()

        return result[0]

    # Подсчитывает кол-во юзеров исключая user_id (Надо для ограничения юзеров на проект)
    def count_all_users(self, user_id) -> int:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        SELECT DISTINCT user_id FROM messages_data WHERE user_id <> ?;
        """

        result = cur.execute(sql_query, (user_id,)).fetchall()

        return len(result)

    def last_row(self, user_id, role):
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        SELECT message FROM messages_data WHERE user_id = ? AND role = ? ORDER BY id DESC LIMIT 1;
        """

        result = cur.execute(
            sql_query,
            (
                user_id,
                role,
            ),
        ).fetchall()

        return result


class UsersDatabase:
    def __init__(self) -> None:
        self.__create_database()

    # Создание БД
    def __create_database(self) -> None:
        self.file_name = user_db
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        CREATE TABLE IF NOT EXISTS users_data(
            user_id INTEGER PRIMARY KEY,
            user_theme TEXT
        );
        """

        cur.execute(sql_query)
        conn.commit()
        conn.close()

    def get_user_theme(self, user_id: int) -> str:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        SELECT user_theme FROM users_data WHERE user_id = ?;
        """

        result = cur.execute(sql_query, (user_id,)).fetchone()

        conn.close()
        return result[0]

    def set_user_theme(self, user_id: int, theme: str) -> None:
        if not self.is_user_registered(user_id):
            self.register_user(user_id)

        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        UPDATE users_data SET user_theme = ? WHERE user_id = ?;
        """

        cur.execute(
            sql_query,
            (
                theme,
                user_id,
            ),
        )

        conn.commit()
        conn.close()

    def is_user_registered(self, user_id: int) -> None:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        SELECT * FROM users_data WHERE user_id = ?;
        """

        result = cur.execute(sql_query, (user_id,)).fetchone()

        conn.close()
        return not (result) is None

    def register_user(self, user_id: int) -> None:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        INSERT INTO users_data(user_id, user_theme) VALUES(?, '');
        """

        cur.execute(sql_query, (user_id,))

        conn.commit()
        conn.close()

    def count_users(self, user_id: int) -> None:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        SELECT user_id FROM users_data WHERE user_id <> ?;
        """

        result = cur.execute(sql_query, (user_id,)).fetchall()

        conn.close()
        return len(result)


class FeedbackDatabase:
    def __init__(self) -> None:
        self.__create_database()

    def __create_database(self) -> None:
        self.file_name = feedback_db
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        CREATE TABLE IF NOT EXISTS feedback_data(
            user_id INTEGER PRIMARY KEY,
            feedback_time TEXT,
            feedback TEXT
        );
        """

        cur.execute(sql_query)
        conn.commit()
        conn.close()

    def set_feedback(self, user_id: int, time: str, feedback: str) -> None:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        INSERT INTO feedback_data(user_id, feedback_time, feedback) VALUES(?, ?, ?);
        """

        cur.execute(
            sql_query,
            (
                user_id,
                time,
                feedback,
            ),
        )
        conn.commit()
        conn.close()

    def is_user_send_feedback(self, user_id: int) -> bool:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        SELECT * FROM feedback_data WHERE user_id = ?;
        """

        result = cur.execute(sql_query, (user_id,)).fetchone()
        conn.close()
        return not result is None

    def user_feedback(self, user_id: int) -> str:
        conn = sqlite3.connect(self.file_name)
        cur = conn.cursor()

        sql_query = """
        SELECT feedback FROM feedback_data WHERE user_id = ?
        """

        result = cur.execute(sql_query, (user_id,)).fetchone()
        conn.close()
        return result
