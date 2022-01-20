
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








