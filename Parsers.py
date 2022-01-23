#Парсим погоду с openweathermap.org.
#Нас интересуют такие параметры в json:
# 1) weather.description
# 2) main.temp, main.feels_like, main.pressure, main.humidity
# 3) wind.speed
# 4) clouds.all
#Регаемся и получаем api-ключ

import requests as req
import json

town = "Ekaterinburg"
api = "42b582831e095766d825429ec639a096"

res = req.get("http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=%s" % (town, api))

#Разбираем код состояния ответа
if res.status_code == 200:
    print("Success!")
elif res.status_code == 404:
    print("Not found")
elif res.status_cod/100 == 4:
    print("4xx: Client Error")
elif res.status_cod/100 == 5:
    print ("5xx: Server Error")


#print(res.headers["Content-Type"]) #Проверяем формат полученных данных

data = res.json()

print("Погода: %s" % data["weather"][0]['description'])
print("Температура: %s *C" % data["main"]["temp"])
print("Ощущается как: %s *C" % data["main"]["feels_like"])
print("Давление: %s hPa" % data["main"]["pressure"])
print("Влажность: %s %%" % data["main"]["humidity"])
print("Скорость ветра: %s м/с" % data["wind"]["speed"])
print("Облачность: %s %%" % data["clouds"]["all"])



#Парсим статитстику преступлений
import csv
cnt = 0
d = {}
#cnt = 0
with open('Crimes.csv', newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        #cnt +=1
        #print (row[2])
        if row[2][6:10] == "2015":
            d[row[5]] = d.setdefault(row[5],0)+1
        #if cnt > 3:
            #break
print(sorted(d.items(), reverse = True, key = lambda x: x[1]),sep = '\n')

#Парсер чисел с numbersapi.com

import requests as req

with open("dataset_24476_3.txt", "r") as f:
    for line in f:
        i = line.strip()
        res = req.get(f'http://numbersapi.com/{i}/math?json=true')
        #print(res.status_code)
        #print(res.headers["Content-Type"])
        if res.json()['found']:
            print("Interesting")
        else:
            print("Boring")

#Парсим артистов с api.artsy.net

import requests
import json

client_id = '4013cd178c5537e0ed79'
client_secret = '4048aea1a8d4eea917633f80e82e9b59'

# инициируем запрос на получение токена
r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                  data={
                      "client_id": client_id,
                      "client_secret": client_secret
                  })

# разбираем ответ сервера
j = json.loads(r.text)

# достаем токен
token = j["token"]
print(token)
# создаем заголовок, содержащий наш токен
headers = {"X-Xapp-Token" : token}
dic = {}
with open("dataset_24476_4.txt", "r") as f:
    for line in f:
        i = line.strip()
        r = requests.get(f"https://api.artsy.net/api/artists/{i}", headers=headers)
        j = json.loads(r.text)
        dic[j['sortable_name']] = j['birthday']

for x in sorted(dic.items(),key = lambda x: x[1]):
    print(x[0])








