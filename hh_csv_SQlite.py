Парсим вакансии с hh. Информация по API тут https://github.com/hhru/api


import requests

# Пакет для удобной работы с данными в формате json
import json

# для записи данных в файл
import csv

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os


def getPage(page=0):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """

    # Справочник для параметров GET-запроса
    params = {
        'text': 'backend python',  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': 3,  # Поиск ощуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 10  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.json()
    return data

#getPage()
with open("вакансии.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
    file_writer.writerow(["Название", "Зарплата", "Требования", "Тип работы",
                          "Дата публикации", "Ссылка на вакансию"])
    # 5 страниц по 10 вакансий с каждой
    for page in range(0, 5):
        x = getPage(page)  # вакансии с одной страницы

        # идем по вакансиям и записываем в cvs по строкам (1 строка - 1 вакансия)
        for vac in range(0, len(x["items"])):
            str1 = [] # массив для информации по одной вакансии

            # название
            str1.append(x["items"][vac]["name"]) #название

            # зарплата
            if x["items"][vac]["salary"] is not None:
                str1.append("от " + str(x["items"][vac]["salary"]["from"]) + \
                         " до " + str(x["items"][vac]["salary"]["to"]))
            else:
                str1.append("не написано")

            #Требования
            str1.append(str(x["items"][vac]["snippet"]["requirement"])+ \
                        str(x["items"][vac]["snippet"]["responsibility"]))

            #Тип работы
            str1.append(str(x["items"][vac]["schedule"]["name"]))

            #Дата публикации
            str1.append(str(x["items"][vac]["published_at"])[:10])

            #URL
            str1.append(str(x["items"][vac]["alternate_url"]))

            #Записываем массив с данными в csv
            file_writer.writerow(str1)

    # Пауза чтобы не заблочили
    time.sleep(0.5)