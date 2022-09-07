from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import csv
surname, name, patronymic = map(str,input().split())

with open('list.csv',mode='w',encoding='Windows-1251') as tabel:
    tabel_writer=csv.writer(tabel,delimiter=';')
    tabel_writer.writerow(['name'])
    tabel_writer.writerow([surname +' '+ name+' ' + patronymic])

tabel = pd.read_csv('list.csv', encoding='Windows-1251') #чтение таблицы и кодировка в Windows-1251
font_1 = ImageFont.truetype('arial.ttf',40) #Шрифт текста, который будет наносится на сертификат. Люблю прописывать это в отдельной переменной, привычка)
font_2 = ImageFont.truetype('arial.ttf',25)
print(tabel.head()) #Вывод содержимого сsv таблицы в терминал. Иногда забываю сохранить, смотрю в терминал и проверяю тем самым, не обязательная строка

for index,j in tabel.iterrows():
    img = Image.open('certificate.jpg') #открытие сертификата
    draw = ImageDraw.Draw(img) #нанесение текста на сертификат
    draw.text(xy=(240,277),text='{}'.format(j['name']),fill=(0,0,0),font=font_1) #настройки наносимого текста, координаты, значение текста
    draw.text(xy=(287,540),text='24.12.2021',fill=(0,0,0),font=font_2)
    img.save('pictures/{}.jpg'.format(j['name'])) #сохранение