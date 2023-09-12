import json

global names
names = {}
global count_names
count_names = 0


def save() -> None:
    """
    Функция сохранения настроек конфигурации.
    Данные сохраняются в формат файла .json.
    """
    with open('data.json', 'w', encoding='utf-8') as json_file:
        data = {'names': names, 'count_names': count_names}
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def load() -> None:
    """
    Функция загрузки настроек конфигурации из .json.
    """
    global names
    global count_names
    with open('data.json', "r", encoding='utf-8') as file:
        data = json.load(file)

    _names = data['names']
    names = {int(key): value for key, value in _names.items()}
    count_names = data['count_names']