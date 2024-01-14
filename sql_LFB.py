import sqlite3
from datetime import datetime
from _db_helper_LFB import get_tables, get_id_table, get_alias, add_db, open_db

main_conn = sqlite3.Connection("LFB.db", check_same_thread=False)
main_cur = main_conn.cursor()
current_datetime = str(datetime.now().day) + "." + str(datetime.now().month) + "." + \
                   str(datetime.now().year) + " " + str(datetime.now().hour) + ":" + \
                   str(datetime.now().minute) + ":" + str(datetime.now().second)


class DataBase:
    def __init__(self, path: str):
        self.path = path
        export_path = path[:-2] + "json"
        code = add_db(path, export_path)
        if code == "error":
            self.connect.close()
            self.__del__()
        else:
            open_db(self.path)
            self.connect = sqlite3.Connection(path, check_same_thread=False)
            self.cursor = self.connect.cursor()
            temp = self.path.split("\\")
            name = temp[-1]
            del temp
            self.name = name
            del name
            self.ddl_items = get_tables(self.name)

    def start(self):
        query = "CREATE TABLE IF NOT EXISTS "
        for table in self.ddl_items:
            query += f"{table} ("
            for row in self.ddl_items[table]:
                query += row + " "
                for param in self.ddl_items[table][row]:
                    if param != "":
                        query += param + " "
                query += ", "
            query += ")"
        self.cursor.execute(query)
        self.connect.commit()

    def find(self, user_id: int):
        table = get_id_table(self.name)
        return self.cursor.execute(f"SELECT id, name FROM {table} WHERE id = {user_id}").fetchone()[0]

    def __str__(self):
        return get_alias(self.name)

    def __call__(self, query, *args):
        self.cursor.execute(query, *args)
        self.connect.commit()

    def __del__(self):
        return "error: file is already exists"


def check_tables():
    main_cur.execute("""CREATE TABLE IF NOT EXISTS feedbacks (
                id       INTEGER NOT NULL,
                name     TEXT    NOT NULL,
                message  TEXT    NOT NULL,
                bot      TEXT    NOT NULL,
                datetime TEXT    NOT NULL
                )""")
    main_conn.commit()
    main_cur.execute("""CREATE TABLE IF NOT EXISTS sent_messages (
                id             INTEGER NOT NULL,
                message_text   TEXT,
                write_datetime TEXT    NOT NULL
                )""")
    main_conn.commit()


def get_info_about_message(user_id, text: str):
    main_cur.execute("INSERT INTO sent_messages (id, message_text, write_datetime) VALUES (?, ?, ?)",
                     (user_id, text, current_datetime))
    main_conn.commit()


def get_record(text: str, user_id: int, name: str, bot: str):
    main_cur.execute("INSERT INTO feedbacks (id, name, message, bot, datetime) VALUES (?, ?, ?, ?, ?)",
                     (user_id, name, text, bot, current_datetime))
    main_conn.commit()


def print_data(*args, **kwargs):
    dst = [*args]
    src = {**kwargs}
    if not dst or not src:
        raise ValueError("Нет условия!")
    query = ""
    for i in dst:
        query += f"SELECT {i} FROM feedbacks WHERE "
        for j in src:
            query += f"{j} = ? AND "
    query = query[:-5:1]
    q_args = tuple(src[i] for i in src)
    temp = main_cur.execute(query, q_args).fetchall()
    result = ""
    for i in temp:
        for j in i:
            result += i[j] + "\n"
    return result


if __name__ == '__main__':
    test = DataBase("C:\\Users\\User\\Documents\\GitHub\\abiturinent-s-folder-bot\\abiturients_folder.db")
    print(str(test))
