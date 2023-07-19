import requests
from bs4 import BeautifulSoup
import re
import json
import pymongo
import time
from fastapi import FastAPI,HTTPException,status
"""start_time = time.time()
# Подключение к MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")


# Выбор базы данных
db = client["nomber"]
collection = db["all_code"]


response = requests.get('https://www.kody.su/mobile/')
soup = BeautifulSoup(response.text, 'lxml')
# pprint(soup)
ij = soup.find('div', class_="content__in").find('p').find_next('p')
all_dict_list = []
for i in ij.find_all('a'):
    cifr = i.text           # 900
    print(cifr)
    print(len(all_dict_list))
    link = i.get('href')    # ссылка

    response = requests.get('https://www.kody.su' + link)
    soup = BeautifulSoup(response.text, 'lxml')
    j_ = soup.find('table', class_="tbnum").find_all('tr')[1:]

    for j in j_:
        list_cod = []

        # Используем регулярное выражение для поиска строк
        pattern = r'<td class="def">(.*?)<'
        matches = re.findall(pattern, str(j))
        # Выводим найденные строки город и оператор
        for match in matches:
            list_cod.append(match.replace('x', '').replace(cifr + '-', ''))



        # Используем регулярное выражение для поиска строк
        pattern = r'<span>(.*?)</span>'
        matches = re.findall(pattern, str(j))

        # Выводим найденные строки
        for match in matches:
            list_cod.append(match.replace('x', ''))

        # print(list_cod)


        td_elements = j.find_all('td')
        # Извлекаем значения
        value1 = td_elements[1].text    # оператор
        value2 = td_elements[2].text    # город

        # print(value1)
        # print(value2)
        for a in list_cod:

            dict_ = {
                'Код': cifr+a,
                'Оператор': value1,
                'Область': value2
            }
            all_dict_list.append(dict_)
            # result = collection.insert_one(dict_)
# Сохраняем список словарей в файл JSON
with open("data.json", "w") as json_file:
    json.dump(all_dict_list, json_file)"""



import pandas as pd
import os
import json
import sys
import time
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import UploadFile
import shutil


app = FastAPI(title='Парсинг номеров')


origins = [
    "http://127.0.0.1:8000/parser"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parser")
async def parser(upload_file:UploadFile):
        try:
            upload_dir = os.path.join(os.getcwd(), "")
            # Create the upload directory if it doesn't exist
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            dest = os.path.join(upload_dir, upload_file.filename)
            print(dest)

            # copy the file contents
            with open(dest, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)

            start_time = time.time()
            print('Начало')
            dict_all_list = []
            # Открываем файл JSON
            with open("/home/anton/Downloads/Telegram Desktop/phone-parser-landing/backend/data.json", "r") as json_file:
                # Загружаем данные из файла JSON
                data_json = json.load(json_file)


            # Чтение Excel-файла
            data = pd.read_excel(f'{upload_file.filename}')

            # Доступ к первой колонке
            for i in data.iloc[:, 0]:
                number_in_sver = str(i)[1:]
                for j in data_json:
                    try:
                        json_code = int(j['Код'])
                        finish_format_numb = int(number_in_sver[:len(str(j['Код']))])
                        if json_code == finish_format_numb:
                            operator = j['Оператор']
                            oblast = j['Область']
                            number = i
                            dict_ = {
                                oblast : number,
                            }
                            dict_all_list.append(dict_)
                            sys.stdout.write(f"\rСтрок в excel: {len(dict_all_list)}")
                            sys.stdout.flush()
                    except:
                        pass


            # Вывод первой колонки
            # print(first_column)
            df = pd.DataFrame(dict_all_list)
            i = 0
            while True:
                try:
                    df.to_excel(f"{upload_file.filename}", index=False)
                    break
                except:
                    i+=1

            end_time = time.time()

            time_diff = end_time - start_time

            days = int(time_diff // (24 * 3600))
            time_diff = time_diff % (24 * 3600)
            hours = int(time_diff // 3600)
            time_diff %= 3600
            minutes = int(time_diff // 60)
            time_diff %= 60
            seconds = round(time_diff)

            time_ = f"\nУспех, время, затраченное на парсинг: \nДней: {days} Часов: {hours} Минут: {minutes} Секунд: {seconds}"
            print(time_)
            return FileResponse(path=f'{upload_file.filename}',filename=f"output.xlsx")

        except Exception as err:
            print(err)


if __name__ == "__main__":
    uvicorn.run(
        'parser:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )