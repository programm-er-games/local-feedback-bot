import pyautogui
import os
import keyboard
from tkinter import messagebox
import json
import pyscreenshot
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pyautogui.FAILSAFE = True

buttons_dict = {
    # "T": 0
}


def _print_json(json_path: str) -> dict:
    with open(json_path, "r") as f:
        result = json.load(f)
        return result


def _get_values(src: dict):
    result = {"db_name": src["name"]}
    temp = {}
    for i in src["objects"]:
        temp[f"table_{i['name']}"] = {"table_name": i["name"], "table_ddl": i["ddl"]}
    result["tables"] = temp
    return result


def _wait_for_user():
    box_name = "Внимание, скрипт!"
    text = "Внимание, сейчас должен выполняться скрипт, " \
           "требующий вмешательства клавиатуры и мыши. Нажмите кнопку \"Ок\", " \
           "чтобы скрипт быстренько сделал своё дело и Вы продолжите работать дальше " \
           "с этим компьютером"
    messagebox.showwarning(box_name, text)


def _error_for_user(error=""):
    box_name = "Внимание, скрипт!"
    text = "Скрипт выполнился c ошибкой!"
    messagebox.showerror(box_name, text, detail=error)


def _finish_for_user():
    box_name = "Внимание, скрипт!"
    text = "Скрипт выполнился! Можете продолжать работу"
    messagebox.showinfo(box_name, text)


def _get_pointer_pixel(x: int, y: int, image):
    return image.getpixel((x, y))


def _get_last_db_button(index=False):
    image = pyscreenshot.grab()
    image.load()
    for i in range(50):
        color = _get_pointer_pixel(26, 130 + (18 * i), image)
        if color == (153, 153, 153) or color == (184, 184, 184):
            # print(26, 130 + (18 * i), color)
            continue
        else:
            # print(26, 130 + (18 * i), color)
            if color == (144, 175, 201):
                return (57, 132 + (18 * i)) if not index else i
            else:
                offset = (i - 1) if i >= 1 else i
                return (57, 132 + (18 * offset)) if not index else offset


def _get_db_button(index: int):
    image = pyscreenshot.grab()
    image.load()
    color = _get_pointer_pixel(26, 130 + (18 * index), image)
    match color:
        case (153, 153, 153) | (184, 184, 184) | (144, 175, 201):
            return 57, 132 + (18 * index)
        case _:
            raise ValueError(f"Кнопка с индексом {index} не найдена!")


def _get_db_button_index(index: int):
    for i in buttons_dict.keys():
        if buttons_dict[i] == index:
            return i


def open_and_connect(path: str, alias: str = ""):
    code = os.system("\"C:\\Program Files\\SQLiteStudio\\SQLiteStudio.exe\"")
    if code == 1:
        raise FileNotFoundError("Неправильно указан путь к файлу!")
    else:
        pyautogui.sleep(1)
        pyautogui.moveTo(48, 32)
        pyautogui.click()
        pyautogui.moveTo(148, 109)
        pyautogui.click()
        pyautogui.moveTo(148, 109)
        pyautogui.click()
        pyautogui.moveTo(869, 488)
        pyautogui.click()
        keyboard.write(path)
        pyautogui.moveTo(868, 549)
        pyautogui.click(clicks=3)
        keyboard.write(alias)
        pyautogui.moveTo(1013, 642)
        pyautogui.click()
        x, y = _get_last_db_button()
        pyautogui.moveTo(x, y)
        pyautogui.click(clicks=2)
        pyautogui.sleep(0.3)
        pyautogui.click(clicks=2)
        buttons_dict[alias if alias else path] = _get_last_db_button(True)
        print(buttons_dict)
        print("Успешно добавлено!")


def disconnect_and_close(button_index: str | int):
    code = os.system("\"C:\\Program Files\\SQLiteStudio\\SQLiteStudio.exe\"")
    if code == 1:
        raise FileNotFoundError("Неправильно указан путь к файлу!")
    else:
        int_btn_index = buttons_dict[button_index] if isinstance(button_index, str) else button_index
        x, y = _get_db_button(int_btn_index)
        pyautogui.moveTo(x, y)
        pyautogui.click(clicks=2)
        pyautogui.moveTo(55, 63)
        pyautogui.click()
        pyautogui.moveTo(x, y)
        keyboard.send("delete")
        keyboard.send("enter")
        str_btn_index = button_index if isinstance(button_index, str) else _get_db_button_index(button_index)
        buttons_dict.pop(str_btn_index)
        print(buttons_dict)
        print("Успешно удалено!")


def export_db_to_json(src_path: str, dst_path: str):
    code = os.system(f"\"{src_path}\"")
    if code == 1:
        raise ValueError("Файл уже существует!")
    x, y = _get_last_db_button()
    pyautogui.moveTo(x, y)
    pyautogui.sleep(0.3)
    pyautogui.click(clicks=2)
    pyautogui.moveTo(421, 59)
    pyautogui.sleep(0.1)
    pyautogui.click()
    pyautogui.moveTo(738, 387)
    pyautogui.sleep(0.1)
    pyautogui.click()
    pyautogui.moveTo(1218, 725)
    pyautogui.sleep(0.1)
    pyautogui.click()
    pyautogui.moveTo(1214, 726)
    pyautogui.sleep(0.1)
    pyautogui.click()
    pyautogui.moveTo(1167, 402)
    pyautogui.sleep(0.1)
    pyautogui.click()
    pyautogui.moveTo(1141, 432)
    pyautogui.sleep(0.1)
    pyautogui.click()
    pyautogui.moveTo(959, 468)
    pyautogui.sleep(0.1)
    pyautogui.click(clicks=3)
    keyboard.write(dst_path)
    pyautogui.moveTo(828, 596)
    pyautogui.sleep(0.1)
    pyautogui.click()
    pyautogui.moveTo(1220, 725)
    pyautogui.sleep(0.1)
    pyautogui.click()
    pyautogui.moveTo(x, y)
    pyautogui.sleep(0.1)
    pyautogui.click()
    keyboard.send("delete")
    pyautogui.sleep(0.1)
    keyboard.send("enter")
    # pyautogui.moveTo(997, 554)
    # pyautogui.sleep(0.2)
    # pyautogui.click()
    print("Успешно экспортировано!")
    return _get_values(_print_json(dst_path))


def execute_script(func, *args):

    def wrapper(*arg_list):
        temp = [*arg_list]
        args_dict = {}
        for i in range(len(temp)):
            args_dict[i] = temp[i]
        temp = []
        for i in args_dict.keys():
            temp.append(i)
        match len(temp):
            case 1: return func(args_dict[0])
            case 2: return func(args_dict[0], args_dict[1])

    try:
        _wait_for_user()
        result = wrapper(*args)
    except (ValueError, FileNotFoundError) as e:
        _error_for_user(e)
    else:
        _finish_for_user()
        return result


def __get_pointer_pos():
    with open("pointer_coords.txt", mode="a+") as f:
        x, y = pyautogui.position()
        f.write(f"{x}; {y}\n")
    return pyautogui.position()


def __set_pointer_pos(x: int, y: int): pyautogui.moveTo(x, y)


def __click(): pyautogui.click()


if __name__ == '__main__':
    # execute_script(export_db_to_json, "C:\\test_dbs\\db_test_0.db", "C:\\test1.json")
    # execute_script(open_and_connect, "C:\\test_dbs\\db_test_0.db", "test")
    # execute_script(disconnect_and_close, buttons_dict["test"])
    # pyautogui.sleep(1)
    # x, y = _get_last_db_button()
    # __set_pointer_pos(x, y)
    # print(export_db_to_json("C:\\test_dbs\\db_test_0.db", "C:\\test1.json"))
    print(__get_pointer_pos())
    # print(_get_pointer_pixel(26, 130))
    # print(_get_last_db_button())
