# Парсим вакансии с hh. Информация по API тут https://github.com/hhru/api
# Сначала парсим в БД SQLlite, потом выгружаем в csv

import requests

# Пакет для удобной работы с данными в формате json
import json

# для записи данных в файл
import csv

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os

import sqlite3

#Подключаемся к БД
conn = sqlite3.connect('vacancies.db') 

cur = conn.cursor()

#Создаем таблицу вакансий, если еще нет
cur.execute("""CREATE TABLE IF NOT EXISTS vacancies_new (
   id TEXT,
   Название TEXT,
   Зарплата TEXT,
   Требования TEXT,
   Тип работы TEXT,
   Дата публикации TEXT,
   Ссылка на вакансию TEXT);
""")
conn.commit()

#  Создаем метод для получения страницы со списком вакансий.
# page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
def getPage(page=0):

    # Справочник для параметров GET-запроса
    params = {
        'text': 'backend python',  # Слова в названии вакансии
        'area': 3,  # Поиск ощуществляется по вакансиям города Екатеринбург
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 10  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.json()
    return data

# getPage()

# 10 страниц по 10 вакансий с каждой
for page in range(0, 10):
    x = getPage(page)  # вакансии с одной страницы

    # идем по вакансиям 
    for vac in range(0, len(x["items"])):
        str1 = []  # массив информации по вакансии для записи в БД

        # id вакансии. Проверяем что такой вакансии нет в базе,
        # если есть то пропускаем добавление
        info = cur.execute('SELECT * FROM vacancies_new WHERE id=?', (x["items"][vac]["id"],))
        if info.fetchone() is None:
            # Если новая то добавляем
            str1.append(x["items"][vac]["id"])

            # название
            str1.append(x["items"][vac]["name"])  # название

            # зарплата
            if x["items"][vac]["salary"] is not None:
                str1.append("от " + str(x["items"][vac]["salary"]["from"]) + \
                            " до " + str(x["items"][vac]["salary"]["to"]))
            else:
                str1.append("не написано")

            # Требования
            str1.append(str(x["items"][vac]["snippet"]["requirement"]) + \
                        str(x["items"][vac]["snippet"]["responsibility"]))

            # Тип работы
            str1.append(str(x["items"][vac]["schedule"]["name"]))

            # Дата публикации
            str1.append(x["items"][vac]["published_at"][:10])

            # URL
            str1.append(x["items"][vac]["alternate_url"])

            # Записываем данные в базу данных
            cur.execute("INSERT INTO vacancies_new VALUES(?, ?, ?, ?, ?, ?, ?);", str1)
            conn.commit()
        else:
            continue

# Пауза чтобы не заблочили
time.sleep(0.5)

#Пишем данные из БД в файл csv
cur.execute("SELECT * FROM vacancies_new;")
one_result = cur.fetchmany(100)

with open("вакансии.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
    file_writer.writerow(["id", "Название", "Зарплата", "Требования", "Тип работы",
                              "Дата публикации", "Ссылка на вакансию"])
    for vac in one_result:
        file_writer.writerow(vac)
        #print(vac)
        
#Всего вакансий        
print(len(one_result)) 
