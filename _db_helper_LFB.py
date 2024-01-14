import os
from _sqlite_work import export_db_to_json, open_and_connect, execute_script

db_dict = {
    # "AF": {
    #     "students": {
    #         "id": ["INTEGER"],
    #         "name": ["TEXT"],
    #         "surname": ["TEXT"],
    #         "patronymic": ["TEXT"],
    #         "phone": ["INTEGER"],
    #         "email": ["TEXT"],
    #         "address": ["TEXT"],
    #         "school": ["TEXT"],
    #         "class": ["TEXT"],
    #         "city": ["TEXT"]
    #     },
    #     "sent_messages": {
    #         "id": ["INTEGER"],
    #         "message_text": ["TEXT"],
    #         "write_datetime": ["TEXT"]
    #     }
    # },
    # "EF": {
    #     "events": {
    #         "name": ["TEXT", "UNIQUE", "NOT NULL"],
    #         "description": ["TEXT"],
    #         "date_start": ["TEXT", "NOT NULL"],
    #         "date_end": ["TEXT", "NOT NULL"],
    #         "contacts": ["TEXT", "NOT NULL"],
    #         "address": ["TEXT", "NOT NULL"],
    #         "add_date": ["TEXT", "NOT NULL"]
    #     },
    #     "participants": {
    #         "id": ["INTEGER", "NOT NULL", "UNIQUE"],
    #         "name": ["TEXT", "NOT NULL", "UNIQUE"],
    #         "surname": ["TEXT", "NOT NULL", "UNIQUE"],
    #         "patronymic": ["TEXT"],
    #         "event_partic": ["TEXT", "NOT NULL"],
    #         "command": ["TEXT", "NOT NULL"],
    #         "organization": ["TEXT", "NOT NULL"],
    #         "email": ["TEXT", "NOT NULL", "UNIQUE"],
    #         "birth_date": ["TEXT", "NOT NULL"],
    #         "add_date": ["TEXT", "NOT NULL"]
    #     },
    #     "sent_messages": {
    #         "id": ["INTEGER", "NOT NULL"],
    #         "message_text": ["TEXT"],
    #         "write_datetime": ["TEXT", "NOT NULL"]
    #     }
    # }
}
db_aliases = {
    # "abiturients_folder.db": "AF",
    # "event_register.db": "EF"
}


def _passage(file_name, folder):
    for element in os.scandir(folder):
        if element.is_file():
            if element.name == file_name:
                yield folder
        else:
            yield from _passage(file_name, element.path)


def scan_directories(name: str):
    temp = _passage(name, "C:\\Users\\User\\Documents\\GitHub")
    result = []
    for i in temp:
        result.append(i)
    return result


def get_tables(db_name: str):
    if db_name in db_aliases.keys():
        return db_dict[db_aliases[db_name]]
    else:
        raise ValueError("Нет такой базы данных в списке!")


def get_id_table(db_name: str):
    if db_name in db_aliases.keys():
        if db_aliases[db_name] == "AF":
            return "students"
        elif db_aliases[db_name] == "EF":
            return "participants"
    else:
        raise ValueError("Нет такой базы данных в списке!")


def get_alias(db_name: str):
    if db_name in db_aliases.keys():
        return db_aliases[db_name]
    else:
        raise ValueError("Нет такой базы данных в списке!")


def add_db_alias(db_name: str, alias: str = ""):
    if not alias:
        temp_db_name = db_name.split("_")
        alias = ""
        for word in temp_db_name:
            is_upper = False
            for i in word:
                if not is_upper:
                    alias += i.capitalize()
                    is_upper = True
                else:
                    alias += i if i.isdigit() else ""
                continue
    if alias:
        db_aliases[db_name] = alias
        print(db_aliases)
        return alias


def add_db(src_path: str, dst_path: str):
    try:
        temp = execute_script(export_db_to_json, src_path, dst_path)
    except ValueError:
        return "error"
    else:
        db_name = add_db_alias(temp["db_name"])
        table_name = []
        table_ddl = []
        r = {db_name: {}}
        for i in temp["tables"].keys():
            table_name.append(temp["tables"][i]["table_name"])
            table_ddl.append(temp["tables"][i]["table_ddl"])
        is_start = False
        is_row = False
        is_param = False
        t = ""
        t_id = ""
        for i in table_name:
            r[db_name][i] = {}
            for ddl in table_ddl:
                for j in ddl:
                    if j == "(":
                        is_start = True
                        continue
                    if is_start:
                        if j.islower() and not is_row:
                            is_row = True
                        if is_row:
                            if j.isspace():
                                t_id = t
                                r[db_name][i].update({t_id: []})
                                t = ""
                                is_row = False
                            else:
                                t += j
                        if j.isupper() and not is_param:
                            is_param = True
                        if is_param:
                            if j.isspace():
                                r[db_name][i][t_id].append(t)
                                t = ""
                            elif j == "," or j == ")":
                                r[db_name][i][t_id].append(t)
                                t = ""
                                is_param = False
                            else:
                                t += j
                    if j == ")":
                        is_start = False
        global db_dict
        db_dict.update(r)
        print(db_dict)


def open_db(path: str): execute_script(open_and_connect, add_db_alias(path))


if __name__ == '__main__':
    open_db("C:/Users/User/Documents/GitHub/backup from Disk D/FB v2.0/feedback_bot_v2.db")
#     add_db("C:\\Users\\User\\Documents\\GitHub\\backup from Disk D\\FB v2.0\\feedback_bot_v2.db", "C:\\test2.json")
#     add_db_alias("feedback_bot_v2")
