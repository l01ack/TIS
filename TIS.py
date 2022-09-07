# -*- coding: utf-8 -*-
import asyncio 																#Ассинхронное программирование   				pip install asyncio
import gspread 																#Работа с Google API   							pip install gspread
from oauth2client.service_account import ServiceAccountCredentials 			#Работа с .json файлом                          pip install google-api-python-client
from googleapiclient.discovery import build 								#Работа с Google Drive       					pip install oauth2client
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload 		#Работа с Google Drive
from PIL import Image, ImageDraw, ImageFont 								#Нанесение текста на сертификат 				pip install pillow
import datetime 															#Работа с датой и временем компьютера
import smtplib 																#Работа с протоколом smtp (рассылка на почту) 	pip install secure-smtplib
import time 																#Работа с временем
import os
import random
from pywebio import start_server    										#Работа с интерфейсом  							pip install pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

link = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']   #Задаем ссылку на Гугл таблици
my_creds = ServiceAccountCredentials.from_json_keyfile_name('task.json', link) 				#Формируем данные для входа из нашего json файла
client = gspread.authorize(my_creds) 														#Запускаем клиент для связи с таблицами
sheet_password = client.open('password').sheet1     #Подключение к таблице с паролем для поподания в админскую панель
password=str(sheet_password.cell(10,6).value)      #Пароль для поподания в админскую панель
sender_mail_log='matholympaid10@gmail.com' 	#Логин от почты отправителя
sender_mail_psw='yuU-6XC-rvm-4mY' 			#Пароль от почты отправителя

async def send_to_mail(): #Отправка результатов на Gmail почту
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    smtp_obj.login(sender_mail_log, sender_mail_psw)  #Логин и пароль от почты отправителя
    smtp_obj.sendmail(sender_mail_log ,recipient_mail, msg.encode('utf-8'))

async def change_mail():  #Замена почт, на которые ведутся рассылки
    if User_data['lesson']=="Математика":
        with use_scope('scope_3', clear=True):
            put_text('Текущий gmail для рассылки результатов тестирование по математике: '+sheet_mails.cell(2,2).value).style('color: black; font-size: 50px,text-align:left')#Старый email
        math_mail = await input('Введите новый gmail, на который будет выполняться рассылка')#Введенение нового email
        sheet_mails.update('B2', math_mail)#изменение таблици с email
        with use_scope('scope_3', clear=True):
            put_text("")
        toast("Gmail успешно обновлён", color="green")

    if User_data['lesson']=="Физика":
        with use_scope('scope_3', clear=True):
            put_text('Текущий gmail для рассылки результатов тестирование по физике: '+sheet_mails.cell(3,2).value).style('color: black; font-size: 50px,text-align:left')#Старый email
        physics_mail = await input('Введите новый gmail, на который будет выполняться рассылка')#Введенение нового email
        sheet_mails.update('B3', physics_mail)#изменение таблици с email
        with use_scope('scope_3', clear=True):
            put_text("")
        toast("Gmail успешно обновлён", color="green")

    if User_data['lesson']=="Информатика":
        with use_scope('scope_3', clear=True):
            put_text('Текущий gmail для рассылки результатов тестирование по информатике: '+sheet_mails.cell(4,2).value).style('color: black; font-size: 50px,text-align:left')#Старый email
        informatics_mail = await input('Введите новый gmail, на который будет выполняться рассылка')#Введенение нового email
        sheet_mails.update('B4', informatics_mail)#изменение таблици с email
        with use_scope('scope_3', clear=True):
            put_text("")
        toast("Gmail успешно обновлён", color="green")

async def AutoCerGen(): #Генерация сертефиката
    global datetime_now
    font_1 = ImageFont.truetype('arial.ttf',110)
    font_3 = ImageFont.truetype('arial.ttf',60)
    datetime_now = datetime.datetime.now()#дата

    if User_data['lesson']=='ПДД' or 'Медицина':
        img = Image.open('AutoCerGen/FLS_for_humans.jpg')
        draw = ImageDraw.Draw(img) 
        draw.text(xy=(320,650),text=User_data['surname'] +' '+User_data['name']+' '+User_data['patronymic'],fill=(0,0,0),font=font_1) #ФИО
        draw.text(xy=(485,1120),text=datetime_now.strftime('%d-%m-%Y'),fill=(0,0,0),font=font_3) #Дата
        draw.text(xy=(1210,1120),text=str(scores)+' баллов',fill=(0,0,0),font=font_3) #Кол-во баллов
        img.save('AutoCerGen/pictures/{}.jpg'.format(User_data['surname'] +' '+User_data['name']+' '+User_data['patronymic'])) #сохранение

    elif post=="Учитель" or post=="Родитель":
        if User_data['lesson']=='Математика':
            img = Image.open('AutoCerGen/Cer_for_humans.jpg')
        if User_data['lesson']=='Физика':
            img = Image.open('AutoCerGen/physics_for_humans.jpg')
        if User_data['lesson']=='Информатика':
            img = Image.open('AutoCerGen/informatics_for_humans.jpg')

        draw = ImageDraw.Draw(img) #нанесение текста на сертификат

        draw.text(xy=(320,650),text=User_data['surname'] +' '+User_data['name']+' '+User_data['patronymic'],fill=(0,0,0),font=font_1) #ФИО
        draw.text(xy=(485,1120),text=datetime_now.strftime('%d-%m-%Y'),fill=(0,0,0),font=font_3) #Дата
        draw.text(xy=(1210,1120),text=str(scores)+' баллов',fill=(0,0,0),font=font_3) #Кол-во баллов
        img.save('AutoCerGen/pictures/{}.jpg'.format(User_data['surname'] +' '+User_data['name']+' '+User_data['patronymic'])) #сохранение

    elif post=="Ученик":
        if User_data['lesson']=='Математика':
            img = Image.open('AutoCerGen/Cer_for_child.jpg')
            draw = ImageDraw.Draw(img) #нанесение текста на сертификат
        if User_data['lesson']=='Физика':
            img = Image.open('AutoCerGen/physics_for_child.jpg')
            draw = ImageDraw.Draw(img) #нанесение текста на сертификат
        if User_data['lesson']=='Информатика':
            img = Image.open('AutoCerGen/informatics_for_child.jpg')
            draw = ImageDraw.Draw(img) #нанесение текста на сертификат

        draw.text(xy=(320,650),text=User_data['surname'] +' '+User_data['name']+' '+User_data['patronymic'],fill=(0,0,0),font=font_1) #ФИО
        draw.text(xy=(485,1150),text=datetime_now.strftime('%d-%m-%Y'),fill=(0,0,0),font=font_3) #Дата
        draw.text(xy=(1210,1150),text=str(scores)+' баллов',fill=(0,0,0),font=font_3) #Кол-во баллов
        if User_data['gender'] == 'Мужской':
            draw.text(xy=(385,825),text='Ученик '+User_data['class']+User_data['letter']+' класса',fill=(0,0,0),font=font_3) #Класс
        elif User_data['gender'] == 'Женский':
            draw.text(xy=(385,825),text='Ученица '+User_data['class']+' '+User_data['letter']+' класса',fill=(0,0,0),font=font_3) #Класс
        draw.text(xy=(1075,830),text='Учитель: '+User_data['teacher'],fill=(0,0,0),font=font_3) #Учитель

        img.save('AutoCerGen/pictures/{}.jpg'.format(User_data['surname'] +' '+User_data['name']+' '+User_data['patronymic'])) #сохранение

async def send_results():
    try:
        if User_data['lesson'] == 'Математика':
            sheet_humans_math=client.open('humans_math').sheet1         #Подключение к таблице с людьми, прошедших тестирование по математике
            L_sheet_humans_math=sheet_humans_math.col_values(8)     #Создание локальной переменной с людьми, прошедших тестирование по математике
            count_tabl=L_sheet_humans_math[0]
            sheet_humans_math.update_cell(count_tabl,1,User_data['surname'])
            sheet_humans_math.update_cell(count_tabl,2,User_data['name'])
            sheet_humans_math.update_cell(count_tabl,3,User_data['patronymic'])
            sheet_humans_math.update_cell(count_tabl,4,post)
            sheet_humans_math.update_cell(count_tabl,5,User_data['class']+User_data['letter'])
            sheet_humans_math.update_cell(count_tabl,6,User_data['school'])
            sheet_humans_math.update_cell(count_tabl,7,scores)
            sheet_humans_math.update('H1',int(count_tabl)+1)

        elif User_data['lesson'] == 'Физика':
            sheet_humans_physics=client.open('humans_physics').sheet1         #Подключение к таблице с людьми, прошедших тестирование по физике
            L_sheet_humans_physics_math=sheet_humans_physics.col_values(8)     #Создание локальной переменной с людьми, прошедших тестирование по физике
            count_tabl=L_sheet_humans_physics[0]
            sheet_humans_physics.update_cell(count_tabl,1,User_data['surname'])
            sheet_humans_physics.update_cell(count_tabl,2,User_data['name'])
            sheet_humans_physics.update_cell(count_tabl,3,User_data['patronymic'])
            sheet_humans_physics.update_cell(count_tabl,4,post)
            sheet_humans_physics.update_cell(count_tabl,5,User_data['class']+User_data['letter'])
            sheet_humans_physics.update_cell(count_tabl,6,User_data['school'])
            sheet_humans_physics.update_cell(count_tabl,7,scores)
            sheet_humans_physics.update('H1',int(count_tabl)+1)
        elif User_data['lesson'] == 'Информатика':
            sheet_humans_inform=client.open('humans_inform').sheet1         #Подключение к таблице с людьми, прошедших тестирование по математике
            L_sheet_humans_inform=sheet_humans_inform.col_values(8)     #Создание локальной переменной с людьми, прошедших тестирование по математике
            count_tabl=L_sheet_humans_inform[0]
            sheet_humans_inform.update_cell(count_tabl,1,User_data['surname'])
            sheet_humans_inform.update_cell(count_tabl,2,User_data['name'])
            sheet_humans_inform.update_cell(count_tabl,3,User_data['patronymic'])
            sheet_humans_inform.update_cell(count_tabl,4,post)
            sheet_humans_inform.update_cell(count_tabl,5,User_data['class']+User_data['letter'])
            sheet_humans_inform.update_cell(count_tabl,6,User_data['school'])
            sheet_humans_inform.update_cell(count_tabl,7,scores)
            sheet_humans_inform.update('H1',int(count_tabl)+1)
        elif User_data['lesson'] == 'Медицина':
            sheet_humans_medic=client.open('Medic_humans').sheet1         #Подключение к таблице с людьми, прошедших тестирование по ОБЖ
            L_sheet_humans_medic=sheet_humans_medic.col_values(8)     #Создание локальной переменной с людьми, прошедших тестирование по ОБЖ
            count_tabl=L_sheet_humans_medic[0]
            sheet_humans_medic.update_cell(count_tabl,1,User_data['surname'])
            sheet_humans_medic.update_cell(count_tabl,2,User_data['name'])
            sheet_humans_medic.update_cell(count_tabl,3,User_data['patronymic'])
            sheet_humans_medic.update_cell(count_tabl,4,post)
            sheet_humans_medic.update_cell(count_tabl,5,User_data['class']+User_data['letter'])
            sheet_humans_medic.update_cell(count_tabl,6,User_data['school'])
            sheet_humans_medic.update_cell(count_tabl,7,scores)
            sheet_humans_medic.update('H1',int(count_tabl)+1)
        elif User_data['lesson'] == 'ПДД':
            sheet_humans_traffic=client.open('traffic_rules_humans').sheet1         #Подключение к таблице с людьми, прошедших тестирование по ОБЖ
            L_sheet_humans_traffic=sheet_humans_traffic.col_values(8)     #Создание локальной переменной с людьми, прошедших тестирование по ОБЖ
            count_tabl=L_sheet_humans_traffic[0]
            sheet_humans_traffic.update_cell(count_tabl,1,User_data['surname'])
            sheet_humans_traffic.update_cell(count_tabl,2,User_data['name'])
            sheet_humans_traffic.update_cell(count_tabl,3,User_data['patronymic'])
            sheet_humans_traffic.update_cell(count_tabl,4,post)
            sheet_humans_traffic.update_cell(count_tabl,5,User_data['class']+User_data['letter'])
            sheet_humans_traffic.update_cell(count_tabl,6,User_data['school'])
            sheet_humans_traffic.update_cell(count_tabl,7,scores)
            sheet_humans_traffic.update('H1',int(count_tabl)+1)
    except:
        time.sleep(5)
        await send_results()#Запись результатов тестирования в таблицу

async def main(): #Главная ф-ция
    global sheet_mails
    try:
        sheet_mails=client.open('mails').sheet1  #Подключение к таблице с email
        L_sheet_mails=sheet_mails.get_all_records()#Создание локальной переменной с email

    except (gspread.exceptions.APIError, gspread.exceptions.SpreadsheetNotFound): #проверка подключения к google sheets
        toast("Не удалось подключиться к googleapiclient", color="red")
        toast("Попытка переподключения...", color="yellow")
        time.sleep(15)
        await main()

    with use_scope('scope_2', clear=True):
        put_text("")
    with use_scope('scope_3', clear=True):
        put_text("")
    with use_scope('scope_4', clear=True):
        put_markdown("")

    with use_scope('scope_1', clear=True):
        put_markdown("## 🧊 Добро пожаловать в Testing_is_simple\n").style('color: black; font-size: 50px,text-align:left')
        await run_login()

async def run_login(): #Выбор должности
    global post
    post=await radio("Кем вы являетесь?",options=["Учитель", "Ученик", "Родитель"]) # выбор должности

    if post==None:
        toast("Выберите одно значение!", color="red")
        await run_login()
    else: await login()

async def login(): #Авторизация пользователя

    if post=="Ученик":

        global User_data,password,word

        User_data=await input_group("Пожалуйста, авторизуйтесь в системе", [  #регистрация
            input("Фамилия", name='surname'), #Фамилия пользователя
            input("Имя", name='name'), #Имя пользователя
            input("Отчество", name='patronymic'), #Отчество пользователя
            select("Пол",["Мужской", "Женский"], name='gender'), #Пол пользователя
            select("Класс", ['5','6','7','8','9','10','11'], name='class'), #Класс пользователя
            select("Буква", ['А','Б','В','Г','Д','Е'], name='letter'), #Буква класса пользователя
            select("Предмет",["Математика", "Физика", "Информатика","ПДД","Медицина"], name='lesson'), #Предмет, по которому будет проводиться тестирование
            #select("Ваш учитель", ['Пономарева С.Ф.','Вакуленко В.С.','Сазонова Г.В.','Батырханов К.М.', 'Суюнчалиева З.М.', 'Колесникова С.В.'], name='teacher'), #Выбор преподавателя пользователя
            input("Полное название образовательного учреждения", name='school') #Образовательное учреждение
            ])

        if User_data['name']=="" or User_data['surname']=="" or User_data['patronymic']=="" or User_data['school']=="" or User_data['gender']==None:#Проверка на заполнение всех полей
            toast("Недостаточно данных!", color="red")
            await login()
        else: await test()

    if post=="Учитель" or post=="Родитель":
        User_data=await input_group("Пожалуйста, авторизуйтесь в системе", [
            input("Фамилия", name='surname'), #Фамилия пользователя
            input("Имя", name='name'), #Имя пользователя
            input("Отчество", name='patronymic'), #Отчество пользователя
            select("Пол",["Мужской", "Женский"], name='gender'), #Пол пользователя
            select("Класс", ['5','6','7','8','9','10','11'], name='class'), #Класс пользователя
            select("Буква", ['А','Б','В','Г','Д','Е'], name='letter'), #Буква класса пользователя
            select("Предмет",["Математика", "Физика", "Информатика","ПДД","Медицина"], name='lesson'), #Предмет, по которому будет проводиться тестирование
            input("Полное название образовательного учреждения", name='school') #Образовательное учреждение
            ])
        if User_data['name']=="" or User_data['surname']=="" or User_data['patronymic']=="" or User_data['school']=="" or User_data['gender']==None: #Проверка на заполнение всех полей
            toast("Недостаточно данных!", color="red")
            await login()
        elif User_data['name']=="admin" and User_data['surname']=="admin" and User_data['patronymic']=="admin" and User_data['school']=="admin": #Вход в панель администратора
            word=str(await input('Введите пароль...'))   #Ввод пароля
            if word==password:          #Проверка пароля
                await admin_panel() #Вход в панель администратора
            else:
                put_text('Вы ввели не верный пароль :(').style('font-size: 20px; font-style: italic')
                put_button(['Вернуться на главную'], onclick=login)#кнопки для возвращения на страницу регистрации
        else: await test()

async def admin_panel(): #Панель администратора

    if User_data['lesson']=='Математика':
        if User_data['class']=='8':
            sheet_math=client.open('math_8').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.col_values(1)       #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
        elif User_data['class']=='7':
            sheet_math=client.open('math_7').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.col_values(1)       #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
        elif User_data['class']=='6':
            sheet_math=client.open('math_6').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.col_values(1)       #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
        elif User_data['class']=='5':
            sheet_math=client.open('math_5').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.col_values(1)      #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
        else:
            sheet_math=client.open('math_tasks').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.col_values(1)       #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
        #sheet_humans_math=client.open('humans_math').sheet1                    #Подключение к таблице с людьми, прошедших тестирование по математике
        #L_sheet_humans_math=sheet_humans_math.get_all_records()                #Создание локальной переменной с людьми, прошедших тестирование по математике
        #sheet_math_full_answers = client.open('math_full_answers').sheet1      #Подключение к таблице с пояснениями к ответам пользователей, прошедших тестирование по математике
        #L_sheet_math_full_answers=sheet_math_full_answers.get_all_records()        #Создание локальной переменной с пояснениями к ответам пользователей, прошедших тестирование по математике

    if User_data['lesson']=='Информатика':
        sheet_informatics = client.open('informatics_tasks').sheet1                         #Подключение к таблице с заданиями тестирования по информатике
        L_sheet_informatics=sheet_informatics.col_values(1)                             #Создание локальной переменной с заданиями тестирования по информатике
        L_sheet_informatics_true=sheet_informatics.col_values(2)
        #sheet_humans_informatics=client.open('humans_inform').sheet1                       #Подключение к таблице с людьми, прошедших тестирование по информатике
        #L_sheet_humans_informatics=sheet_humans_informatics.get_all_records()              #Создание локальной переменной с людьми, прошедших тестирование по информатике
        #sheet_informatics_full_answers=client.open('informatics_full_answers').sheet1      #Подключение к таблице с пояснениями к ответам пользователей, прошедших тестирование по информатике
        #L_sheet_informatics_full_answers=sheet_informatics_full_answers.get_all_records()  #Создание локальной переменной с пояснениями к ответам пользователей, прошедших тестирование по информатике

    if User_data['lesson']=='Физика':
        sheet_physics = client.open('physics_tasks').sheet1                         #Подключение к таблице с заданиями тестирования по физике
        L_sheet_physics=sheet_physics.col_values(1)                                 #Создание локальной переменной с заданиями тестирования по физике
        L_sheet_physics_A=sheet_physics.col_values(2)
        L_sheet_physics_B=sheet_physics.col_values(3)
        L_sheet_physics_C=sheet_physics.col_values(4)
        L_sheet_physics_D=sheet_physics.col_values(5)
        L_sheet_physics_E=sheet_physics.col_values(6)
        L_sheet_physics_F=sheet_physics.col_values(7)
        L_sheet_physics_true=sheet_physics.col_values(8)
        #sheet_humans_physics=client.open('humans_physics').sheet1                  #Подключение к таблице с людьми, прошедших тестирование по физике
        #L_sheet_humans_physics=sheet_humans_physics.get_all_records()              #Создание локальной переменной с людьми, прошедших тестирование по физике
        #sheet_physics_full_answers=client.open('physics_full_answers').sheet1      #Подключение к таблице с пояснениями к ответам пользователей, прошедших тестирование по физике
        #L_sheet_physics_full_answers=sheet_physics_full_answers.get_all_records()  #Создание локальной переменной с пояснениями к ответам пользователей, прошедших тестирование по физике
    if User_data['lesson']=='Медицина': 
        sheet_medic = client.open('Medic').sheet1                         #Подключение к таблице с заданиями тестирования по медицине
        L_sheet_medic=sheet_physics.col_values(1)                                 #Создание локальной переменной с заданиями тестирования по медицине
        L_sheet_medic_A=sheet_medic.col_values(2)
        L_sheet_medic_B=sheet_medic.col_values(3)
        L_sheet_medic_C=sheet_medic.col_values(4)
        L_sheet_medic_D=sheet_medic.col_values(5)
        L_sheet_medic_E=sheet_medic.col_values(6)
        L_sheet_medic_F=sheet_medic.col_values(7)
        L_sheet_medic_true=sheet_medic.col_values(8)
    if User_data['lesson']=='ПДД':
        sheet_traffic = client.open('traffic_rules').sheet1                         #Подключение к таблице с заданиями тестирования по ПДД
        L_sheet_traffic=sheet_traffic.col_values(1)                                 #Создание локальной переменной с заданиями тестирования по ПДД
        L_sheet_traffic_A=sheet_traffic.col_values(2)
        L_sheet_traffic_B=sheet_traffic.col_values(3)
        L_sheet_traffic_C=sheet_traffic.col_values(4)
        L_sheet_traffic_D=sheet_traffic.col_values(5)
        L_sheet_traffic_E=sheet_traffic.col_values(6)
        L_sheet_traffic_F=sheet_traffic.col_values(7)
        L_sheet_traffic_true=sheet_traffic.col_values(8)


    async def retask_1():  	#Изменение 1-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №1\n'+str(L_sheet_math[1]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №1\n'+str(L_sheet_math_true[1]))#Текущий ответ задачи
                T1=await input_group("", [
                input("Введите новое условие задачи №1", name='task_1'),#Ввод нового условия для задачи
                input("Введите новый ответ задачи №1", name='true_1'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Физика":
                put_text('\nТекущие условие задачи №1\n'+str(L_sheet_physics[1]))#Текущие условия задачи
                put_text('\nТекущий варианты к задаче №1\n'+str(L_sheet_physics_A[1])+'\n'+str(L_sheet_physics_B[1])+'\n'+str(L_sheet_physics_C[1])+'\n'+str(L_sheet_physics_D[1])+'\n'+str(L_sheet_physics_E[1])+'\n'+str(L_sheet_physics_F[1]))#Текущий варианты к задаче
                put_text('\nТекущий правильный ответ к задаче №1\n'+str(L_sheet_physics_true[1]))#Текущий ответ задачи
                T1=await input_group("", [
                input("Введите новое условие задачи №1", name='task_1'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №1", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №1", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №1", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №1", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №1", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №1", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №1", name='true_1'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №1\n'+str(L_sheet_informatics[1]))#Текущие условия задачи
                put_text('\nТекущий ответ к задаче №1\n'+str(L_sheet_informatics_true[1]))#Текущий ответ задачи
                T1=await input_group("", [
                input("Введите новое условие задачи №1", name='task_1'),#Ввод нового условия для задачи
                input("Введите новый ответ задачи №1", name='true_1'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']=="Медицина":
                    put_text('\nТекущие условие задачи №1\n'+str(L_sheet_medic[1]))#Текущие условия задачи
                    put_text('\nТекущий варианты к задаче №1\n'+str(L_sheet_medic_A[1])+'\n'+str(L_sheet_medic_B[1])+'\n'+str(L_sheet_medic_C[1])+'\n'+str(L_sheet_medic_D[1])+'\n'+str(L_sheet_medic_E[1])+'\n'+str(L_sheet_medic_F[1]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №1\n'+str(L_sheet_medic_true[1]))#Текущий ответ задачи
                elif User_data['lesson']=="ПДД":
                    put_text('\nТекущие условие задачи №1\n'+str(L_sheet_medic[1]))#Текущие условия задачи
                    put_text('\nТекущий варианты к задаче №1\n'+str(L_sheet_medic_A[1])+'\n'+str(L_sheet_medic_B[1])+'\n'+str(L_sheet_medic_C[1])+'\n'+str(L_sheet_medic_D[1])+'\n'+str(L_sheet_medic_E[1])+'\n'+str(L_sheet_medic_F[1]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №1\n'+str(L_sheet_medic_true[1]))#Текущий ответ задачи
                T1=await input_group("", [
                input("Введите новое условие задачи №1", name='task_1'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №1", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №1", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №1", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №1", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №1", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №1", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №1", name='true_1'),#Ввод нового ответа для задачи
                ])

            if User_data['lesson']=="Математика":       #Обновление таблицы с задачами
                sheet_math.update('A2',T1['task_1'])
                sheet_math.update('B2',T1['true_1'])
            if User_data['lesson']=="Физика":           #Обновление таблицы с задачами
                sheet_physics.update('A2',T1['task_1'])
                sheet_physics.update('H2',T1['true_1'])
                sheet_physics.update('B2',T1['A'])
                sheet_physics.update('C2',T1['B'])
                sheet_physics.update('D2',T1['C'])
                sheet_physics.update('E2',T1['D'])
                sheet_physics.update('F2',T1['E'])
                sheet_physics.update('G2',T1['F'])
            if User_data['lesson']=="Информатика":      #Обновление таблицы с задачами
                sheet_informatics.update('A2',T1['task_1'])
                sheet_informatics.update('B2',T1['true_1'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A2',T1['task_1'])
                sheet_medic.update('H2',T1['true_1'])
                sheet_medic.update('B2',T1['A'])
                sheet_medic.update('C2',T1['B'])
                sheet_medic.update('D2',T1['C'])
                sheet_medic.update('E2',T1['D'])
                sheet_medic.update('F2',T1['E'])
                sheet_medic.update('G2',T1['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A2',T1['task_1'])
                sheet_traffic.update('H2',T1['true_1'])
                sheet_traffic.update('B2',T1['A'])
                sheet_traffic.update('C2',T1['B'])
                sheet_traffic.update('D2',T1['C'])
                sheet_traffic.update('E2',T1['D'])
                sheet_traffic.update('F2',T1['E'])
                sheet_traffic.update('G2',T1['F'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 1 успешно обновлено', color="green")
    async def retask_2(): 	#Изменение 2-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №2\n'+str(L_sheet_math[2]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №2\n'+str(L_sheet_math_true[2]))#Текущий ответ задачи
            if User_data['lesson']=="Физика" or User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']=="Физика":
                    put_text('\nТекущие условие задачи №2\n'+str(L_sheet_physics[2]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №2\n'+str(L_sheet_physics_A[2])+'\n'+str(L_sheet_physics_B[2])+'\n'+str(L_sheet_physics_C[2])+'\n'+str(L_sheet_physics_D[2])+'\n'+str(L_sheet_physics_E[2])+'\n'+str(L_sheet_physics_F[2]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №2\n'+str(L_sheet_physics_true[2]))#Текущий ответ задачи
                if User_data['lesson']=="Медицина":
                    put_text('\nТекущие условие задачи №2\n'+str(L_sheet_medic[2]))#Текущие условия задачи
                    put_text('\nТекущий варианты к задаче №2\n'+str(L_sheet_medic_A[2])+'\n'+str(L_sheet_medic_B[2])+'\n'+str(L_sheet_medic_C[2])+'\n'+str(L_sheet_medic_D[2])+'\n'+str(L_sheet_medic_E[2])+'\n'+str(L_sheet_medic_F[2]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №2\n'+str(L_sheet_medic_true[2]))#Текущий ответ задачи
                if User_data['lesson']=="ПДД":
                    put_text('\nТекущие условие задачи №2\n'+str(L_sheet_traffic[2]))#Текущие условия задачи
                    put_text('\nТекущий варианты к задаче №2\n'+str(L_sheet_traffic_A[2])+'\n'+str(L_sheet_traffic_B[2])+'\n'+str(L_sheet_traffic_C[2])+'\n'+str(L_sheet_traffic_D[2])+'\n'+str(L_sheet_traffic_E[2])+'\n'+str(L_sheet_traffic_F[2]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №2\n'+str(L_sheet_traffic_true[2]))#Текущий ответ задачи
                T2=await input_group("", [
                input("Введите новое условие задачи №2", name='task_2'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №2", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №2", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №2", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №2", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №2", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №2", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №2", name='true_2'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №2\n'+str(L_sheet_informatics[2]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №2\n'+str(L_sheet_informatics_true[2]))#Текущий ответ задачи
            if User_data['lesson']!="Физика" or User_data['lesson']!="Медицина" or User_data['lesson']!="ПДД":
                T2=await input_group("", [
                    input("Введите новое условие задачи №2", name='task_2'),#Ввод нового условия для задачи
                    input("Введите новый ответ задачи №2", name='true_2'),#Ввод нового ответа для задачи
                    ])
            if User_data['lesson']=="Математика":#Обновление таблицы с задачами
                sheet_math.update('A3',T2['task_2'])
                sheet_math.update('B3',T2['true_2'])
            if User_data['lesson']=="Физика":#Обновление таблицы с задачами
                sheet_physics.update('A3',T2['task_2'])
                sheet_physics.update('H3',T2['true_2'])
                sheet_physics.update('B3',T2['A'])
                sheet_physics.update('C3',T2['B'])
                sheet_physics.update('D3',T2['C'])
                sheet_physics.update('E3',T2['D'])
                sheet_physics.update('F3',T2['E'])
                sheet_physics.update('G3',T2['F'])
            if User_data['lesson']=="Информатика":#Обновление таблицы с задачами
                sheet_informatics.update('A3',T2['task_2'])
                sheet_informatics.update('B3',T2['true_2'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A3',T2['task_2'])
                sheet_medic.update('H3',T2['true_2'])
                sheet_medic.update('B3',T2['A'])
                sheet_medic.update('C3',T2['B'])
                sheet_medic.update('D3',T2['C'])
                sheet_medic.update('E3',T2['D'])
                sheet_medic.update('F3',T2['E'])
                sheet_medic.update('G3',T2['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A3',T2['task_2'])
                sheet_traffic.update('H3',T2['true_2'])
                sheet_traffic.update('B3',T2['A'])
                sheet_traffic.update('C3',T2['B'])
                sheet_traffic.update('D3',T2['C'])
                sheet_traffic.update('E3',T2['D'])
                sheet_traffic.update('F3',T2['E'])
                sheet_traffic.update('G3',T2['F'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 2 успешно обновлено', color="green")
    async def retask_3(): 	#Изменение 3-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №3\n'+str(L_sheet_math[3]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №3\n'+str(L_sheet_math_true[3]))#Текущий ответ задачи
            if User_data['lesson']=="Физика" or User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']=="Физика":
                    put_text('\nТекущие условие задачи №3\n'+str(L_sheet_physics[3]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №3\n'+str(L_sheet_physics_A[3])+'\n'+str(L_sheet_physics_B[3])+'\n'+str(L_sheet_physics_C[3])+'\n'+str(L_sheet_physics_D[3])+'\n'+str(L_sheet_physics_E[3])+'\n'+str(L_sheet_physics_F[3]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №3\n'+str(L_sheet_physics_true[3]))#Текущий ответ задачи
                elif User_data['lesson']== "Медицина":
                    put_text('\nТекущие условие задачи №3\n'+str(L_sheet_medic[3]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №3\n'+str(L_sheet_medic_A[3])+'\n'+str(L_sheet_medic_B[3])+'\n'+str(L_sheet_medic_C[3])+'\n'+str(L_sheet_medic_D[3])+'\n'+str(L_sheet_medic_E[3])+'\n'+str(L_sheet_medic_F[3]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №3\n'+str(L_sheet_medic_true[3]))#Текущий ответ задачи
                elif User_data['lesson']== "ПДД":
                    put_text('\nТекущие условие задачи №3\n'+str(L_sheet_traffic[3]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №3\n'+str(L_sheet_traffic_A[3])+'\n'+str(L_sheet_traffic_B[3])+'\n'+str(L_sheet_traffic_C[3])+'\n'+str(L_sheet_traffic_D[3])+'\n'+str(L_sheet_traffic_E[3])+'\n'+str(L_sheet_traffic_F[3]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №3\n'+str(L_sheet_traffic_true[3]))#Текущий ответ задачи
                T3=await input_group("", [
                input("Введите новое условие задачи №3", name='task_3'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №3", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №3", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №3", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №3", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №3", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №3", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №3", name='true_3'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №3\n'+str(L_sheet_informatics[3]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №3\n'+str(L_sheet_informatics_true[3]))#Текущий ответ задачи
            if User_data['lesson']!="Физика" or User_data['lesson']!="Медицина" or User_data['lesson']!="ПДД":
                T3=await input_group("", [
                    input("Введите новое условие задачи №3", name='task_3'),#Ввод нового условия для задачи
                    input("Введите новый ответ задачи №3", name='true_3'),#Ввод нового ответа для задачи
                    ])
            if User_data['lesson']=="Математика":#Обновление таблицы с задачами
                sheet_math.update('A4',T3['task_3'])
                sheet_math.update('B4',T3['true_3'])
            if User_data['lesson']=="Физика":#Обновление таблицы с задачами
                sheet_physics.update('A4',T3['task_3'])
                sheet_physics.update('H4',T3['true_3'])
                sheet_physics.update('B4',T3['A'])
                sheet_physics.update('C4',T3['B'])
                sheet_physics.update('D4',T3['C'])
                sheet_physics.update('E4',T3['D'])
                sheet_physics.update('F4',T3['E'])
                sheet_physics.update('G4',T3['F'])
            if User_data['lesson']=="Информатика":#Обновление таблицы с задачами
                sheet_informatics.update('A4',T3['task_3'])
                sheet_informatics.update('B4',T3['true_3'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A4',T3['task_3'])
                sheet_medic.update('H4',T3['true_3'])
                sheet_medic.update('B4',T3['A'])
                sheet_medic.update('C4',T3['B'])
                sheet_medic.update('D4',T3['C'])
                sheet_medic.update('E4',T3['D'])
                sheet_medic.update('F4',T3['E'])
                sheet_medic.update('G4',T3['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A4',T3['task_3'])
                sheet_traffic.update('H4',T3['true_3'])
                sheet_traffic.update('B4',T3['A'])
                sheet_traffic.update('C4',T3['B'])
                sheet_traffic.update('D4',T3['C'])
                sheet_traffic.update('E4',T3['D'])
                sheet_traffic.update('F4',T3['E'])
                sheet_traffic.update('G4',T3['F'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 3 успешно обновлено', color="green")
    async def retask_4(): 	#Изменение 4-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №4\n'+str(L_sheet_math[4]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №4\n'+str(L_sheet_math_true[4]))#Текущий ответ задачи
            if User_data['lesson']=="Физика" or User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']=="Физика":
                    put_text('\nТекущие условие задачи №4\n'+str(L_sheet_physics[4]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №4\n'+str(L_sheet_physics_A[4])+'\n'+str(L_sheet_physics_B[4])+'\n'+str(L_sheet_physics_C[4])+'\n'+str(L_sheet_physics_D[4])+'\n'+str(L_sheet_physics_E[4])+'\n'+str(L_sheet_physics_F[4]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №4\n'+str(L_sheet_physics_true[4]))#Текущий ответ задачи
                elif User_data['lesson']== "Медицина":
                    put_text('\nТекущие условие задачи №4\n'+str(L_sheet_medic[4]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №4\n'+str(L_sheet_medic_A[4])+'\n'+str(L_sheet_medic_B[4])+'\n'+str(L_sheet_medic_C[4])+'\n'+str(L_sheet_medic_D[4])+'\n'+str(L_sheet_medic_E[4])+'\n'+str(L_sheet_medic_F[4]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №4\n'+str(L_sheet_medic_true[4]))#Текущий ответ задачи
                elif User_data['lesson']== "ПДД":
                    put_text('\nТекущие условие задачи №4\n'+str(L_sheet_traffic[4]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №4\n'+str(L_sheet_traffic_A[4])+'\n'+str(L_sheet_traffic_B[4])+'\n'+str(L_sheet_traffic_C[4])+'\n'+str(L_sheet_traffic_D[4])+'\n'+str(L_sheet_traffic_E[4])+'\n'+str(L_sheet_traffic_F[4]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №4\n'+str(L_sheet_traffic_true[4]))#Текущий ответ задачи
                T4=await input_group("", [
                input("Введите новое условие задачи №4", name='task_4'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №4", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №4", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №4", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №4", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №4", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №4", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №4", name='true_4'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №4\n'+str(L_sheet_informatics[4]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №4\n'+str(L_sheet_informatics_true[4]))#Текущий ответ задачи
            if User_data['lesson']!="Физика" or User_data['lesson']!="Медицина" or User_data['lesson']!="ПДД":
                T4=await input_group("", [
                    input("Введите новое условие задачи №4", name='task_4'),#Ввод нового условия для задачи
                    input("Введите новый ответ задачи №4", name='true_4'),#Ввод нового ответа для задачи
                    ])
            if User_data['lesson']=="Математика":#Обновление таблицы с задачами
                sheet_math.update('A5',T4['task_4'])
                sheet_math.update('B5',T4['true_4'])
            if User_data['lesson']=="Физика":#Обновление таблицы с задачами
                sheet_physics.update('A5',T4['task_4'])
                sheet_physics.update('H5',T4['true_4'])
                sheet_physics.update('B5',T4['A'])
                sheet_physics.update('C5',T4['B'])
                sheet_physics.update('D5',T4['C'])
                sheet_physics.update('E5',T4['D'])
                sheet_physics.update('F5',T4['E'])
                sheet_physics.update('G5',T4['F'])
            if User_data['lesson']=="Информатика":#Обновление таблицы с задачами
                sheet_informatics.update('A5',T4['task_4'])
                sheet_informatics.update('B5',T4['true_4'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A5',T4['task_4'])
                sheet_medic.update('H5',T4['true_4'])
                sheet_medic.update('B5',T4['A'])
                sheet_medic.update('C5',T4['B'])
                sheet_medic.update('D5',T4['C'])
                sheet_medic.update('E5',T4['D'])
                sheet_medic.update('F5',T4['E'])
                sheet_medic.update('G5',T4['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A5',T4['task_4'])
                sheet_traffic.update('H5',T4['true_4'])
                sheet_traffic.update('B5',T4['A'])
                sheet_traffic.update('C5',T4['B'])
                sheet_traffic.update('D5',T4['C'])
                sheet_traffic.update('E5',T4['D'])
                sheet_traffic.update('F5',T4['E'])
                sheet_traffic.update('G5',T4['F'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 4 успешно обновлено', color="green")
    async def retask_5(): 	#Изменение 5-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №5\n'+str(L_sheet_math[5]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №5\n'+str(L_sheet_math_true[5]))#Текущий ответ задачи
            if User_data['lesson']=="Физика" or User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']=="Физика":
                    put_text('\nТекущие условие задачи №5\n'+str(L_sheet_physics[5]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №5\n'+str(L_sheet_physics_A[5])+'\n'+str(L_sheet_physics_B[5])+'\n'+str(L_sheet_physics_C[5])+'\n'+str(L_sheet_physics_D[5])+'\n'+str(L_sheet_physics_E[5])+'\n'+str(L_sheet_physics_F[5]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №5\n'+str(L_sheet_physics_true[5]))#Текущий ответ задачи
                elif User_data['lesson']== "Медицина":
                    put_text('\nТекущие условие задачи №5\n'+str(L_sheet_medic[5]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №5\n'+str(L_sheet_medic_A[5])+'\n'+str(L_sheet_medic_B[5])+'\n'+str(L_sheet_medic_C[5])+'\n'+str(L_sheet_medic_D[5])+'\n'+str(L_sheet_medic_E[5])+'\n'+str(L_sheet_medic_F[5]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №5\n'+str(L_sheet_medic_true[5]))#Текущий ответ задачи
                elif User_data['lesson']== "ПДД":
                    put_text('\nТекущие условие задачи №5\n'+str(L_sheet_traffic[5]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №5\n'+str(L_sheet_traffic_A[5])+'\n'+str(L_sheet_traffic_B[5])+'\n'+str(L_sheet_traffic_C[5])+'\n'+str(L_sheet_traffic_D[5])+'\n'+str(L_sheet_traffic_E[5])+'\n'+str(L_sheet_traffic_F[5]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №5\n'+str(L_sheet_traffic_true[5]))#Текущий ответ задачи
                T5=await input_group("", [
                input("Введите новое условие задачи №5", name='task_5'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №5", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №5", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №5", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №5", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №5", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №5", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №5", name='true_5'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №5\n'+str(L_sheet_informatics[5]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №5\n'+str(L_sheet_informatics_true[5]))#Текущий ответ задачи
            if User_data['lesson']!="Физика" or User_data['lesson']!="Медицина" or User_data['lesson']!="ПДД":
                T5=await input_group("", [
                    input("Введите новое условие задачи №5", name='task_5'),#Ввод нового условия для задачи
                    input("Введите новый ответ задачи №5", name='true_5'),#Ввод нового ответа для задачи
                    ])
            if User_data['lesson']=="Математика":#Обновление таблицы с задачами
                sheet_math.update('A6',T5['task_5'])
                sheet_math.update('B6',T5['true_5'])
            if User_data['lesson']=="Физика":#Обновление таблицы с задачами
                sheet_physics.update('A6',T5['task_5'])
                sheet_physics.update('H6',T5['true_5'])
                sheet_physics.update('B6',T5['A'])
                sheet_physics.update('C6',T5['B'])
                sheet_physics.update('D6',T5['C'])
                sheet_physics.update('E6',T5['D'])
                sheet_physics.update('F6',T5['E'])
                sheet_physics.update('G6',T5['F'])
            if User_data['lesson']=="Информатика":#Обновление таблицы с задачами
                sheet_informatics.update('A6',T5['task_5'])
                sheet_informatics.update('B6',T5['true_5'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A6',T5['task_5'])
                sheet_medic.update('H6',T5['true_5'])
                sheet_medic.update('B6',T5['A'])
                sheet_medic.update('C6',T5['B'])
                sheet_medic.update('D6',T5['C'])
                sheet_medic.update('E6',T5['D'])
                sheet_medic.update('F6',T5['E'])
                sheet_medic.update('G6',T5['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A6',T5['task_5'])
                sheet_traffic.update('H6',T5['true_5'])
                sheet_traffic.update('B6',T5['A'])
                sheet_traffic.update('C6',T5['B'])
                sheet_traffic.update('D6',T5['C'])
                sheet_traffic.update('E6',T5['D'])
                sheet_traffic.update('F6',T5['E'])
                sheet_traffic.update('G6',T5['F'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 5 успешно обновлено', color="green")
    async def retask_6(): 	#Изменение 6-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №6\n'+str(L_sheet_math[6]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №6\n'+str(L_sheet_math_true[6]))#Текущий ответ задачи
            if User_data['lesson']=="Физика" or User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']=="Физика":
                    put_text('\nТекущие условие задачи №6\n'+str(L_sheet_physics[6]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №6\n'+str(L_sheet_physics_A[6])+'\n'+str(L_sheet_physics_B[6])+'\n'+str(L_sheet_physics_C[6])+'\n'+str(L_sheet_physics_D[6])+'\n'+str(L_sheet_physics_E[6])+'\n'+str(L_sheet_physics_F[6]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №6\n'+str(L_sheet_physics_true[6]))#Текущий ответ задачи
                elif User_data['lesson']== "Медицина":
                    put_text('\nТекущие условие задачи №6\n'+str(L_sheet_medic[6]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №6\n'+str(L_sheet_medic_A[6])+'\n'+str(L_sheet_medic_B[6])+'\n'+str(L_sheet_medic_C[6])+'\n'+str(L_sheet_medic_D[6])+'\n'+str(L_sheet_medic_E[6])+'\n'+str(L_sheet_medic_F[6]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №6\n'+str(L_sheet_medic_true[6]))#Текущий ответ задачи
                elif User_data['lesson']== "ПДД":
                    put_text('\nТекущие условие задачи №6\n'+str(L_sheet_traffic[6]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №6\n'+str(L_sheet_traffic_A[6])+'\n'+str(L_sheet_traffic_B[6])+'\n'+str(L_sheet_traffic_C[6])+'\n'+str(L_sheet_traffic_D[6])+'\n'+str(L_sheet_traffic_E[6])+'\n'+str(L_sheet_traffic_F[6]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №6\n'+str(L_sheet_traffic_true[6]))#Текущий ответ задачи
                T6=await input_group("", [
                input("Введите новое условие задачи №6", name='task_6'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №6", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №6", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №6", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №6", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №6", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №6", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №6", name='true_6'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №6\n'+str(L_sheet_informatics[6]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №6\n'+str(L_sheet_informatics_true[6]))#Текущий ответ задачи
            if User_data['lesson']!="Физика" or User_data['lesson']!="Медицина" or User_data['lesson']!="ПДД":
                T6=await input_group("", [
                    input("Введите новое условие задачи №6", name='task_6'),#Ввод нового условия для задачи
                    input("Введите новый ответ задачи №6", name='true_6'),#Ввод нового ответа для задачи
                    ])
            if User_data['lesson']=="Математика":#Обновление таблицы с задачами
                sheet_math.update('A7',T6['task_6'])
                sheet_math.update('B7',T6['true_6'])
            if User_data['lesson']=="Физика":#Обновление таблицы с задачами
                sheet_physics.update('A7',T6['task_6'])
                sheet_physics.update('H7',T6['true_6'])
                sheet_physics.update('B7',T6['A'])
                sheet_physics.update('C7',T6['B'])
                sheet_physics.update('D7',T6['C'])
                sheet_physics.update('E7',T6['D'])
                sheet_physics.update('F7',T6['E'])
                sheet_physics.update('G7',T6['F'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A7',T6['task_6'])
                sheet_medic.update('H7',T6['true_6'])
                sheet_medic.update('B7',T6['A'])
                sheet_medic.update('C7',T6['B'])
                sheet_medic.update('D7',T6['C'])
                sheet_medic.update('E7',T6['D'])
                sheet_medic.update('F7',T6['E'])
                sheet_medic.update('G7',T6['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A7',T6['task_6'])
                sheet_traffic.update('H7',T6['true_6'])
                sheet_traffic.update('B7',T6['A'])
                sheet_traffic.update('C7',T6['B'])
                sheet_traffic.update('D7',T6['C'])
                sheet_traffic.update('E7',T6['D'])
                sheet_traffic.update('F7',T6['E'])
                sheet_traffic.update('G7',T6['F'])
            if User_data['lesson']=="Информатика":#Обновление таблицы с задачами
                sheet_informatics.update('A7',T6['task_6'])
                sheet_informatics.update('B7',T6['true_6'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 6 успешно обновлено', color="green")
    async def retask_7(): 	#Изменение 7-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №7\n'+str(L_sheet_math[7]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №7\n'+str(L_sheet_math_true[7]))#Текущий ответ задачи
            if User_data['lesson']=="Физика" or User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']=="Физика":
                    put_text('\nТекущие условие задачи №7\n'+str(L_sheet_physics[7]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №7\n'+str(L_sheet_physics_A[7])+'\n'+str(L_sheet_physics_B[7])+'\n'+str(L_sheet_physics_C[7])+'\n'+str(L_sheet_physics_D[7])+'\n'+str(L_sheet_physics_E[7])+'\n'+str(L_sheet_physics_F[7]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №7\n'+str(L_sheet_physics_true[7]))#Текущий ответ задачи
                elif User_data['lesson']== "Медицина":
                    put_text('\nТекущие условие задачи №7\n'+str(L_sheet_medic[7]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №7\n'+str(L_sheet_medic_A[7])+'\n'+str(L_sheet_medic_B[7])+'\n'+str(L_sheet_medic_C[7])+'\n'+str(L_sheet_medic_D[7])+'\n'+str(L_sheet_medic_E[7])+'\n'+str(L_sheet_medic_F[7]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №7\n'+str(L_sheet_medic_true[7]))#Текущий ответ задачи
                elif User_data['lesson']== "ПДД":
                    put_text('\nТекущие условие задачи №7\n'+str(L_sheet_traffic[7]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №7\n'+str(L_sheet_traffic_A[7])+'\n'+str(L_sheet_traffic_B[7])+'\n'+str(L_sheet_traffic_C[7])+'\n'+str(L_sheet_traffic_D[7])+'\n'+str(L_sheet_traffic_E[7])+'\n'+str(L_sheet_traffic_F[7]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №7\n'+str(L_sheet_traffic_true[7]))#Текущий ответ задачи
                T7=await input_group("", [
                input("Введите новое условие задачи №7", name='task_7'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №7", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №7", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №7", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №7", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №7", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №7", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №7", name='true_7'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №7\n'+str(L_sheet_informatics[7]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №7\n'+str(L_sheet_informatics_true[7]))#Текущий ответ задачи
            if User_data['lesson']!="Физика" or User_data['lesson']!="Медицина" or User_data['lesson']!="ПДД":
                T7=await input_group("", [
                    input("Введите новое условие задачи №7", name='task_7'),#Ввод нового условия для задачи
                    input("Введите новый ответ задачи №7", name='true_7'),#Ввод нового ответа для задачи
                    ])
            if User_data['lesson']=="Математика":#Обновление таблицы с задачами
                sheet_math.update('A8',T7['task_7'])
                sheet_math.update('B8',T7['true_7'])
            if User_data['lesson']=="Физика":#Обновление таблицы с задачами
                sheet_physics.update('A8',T7['task_7'])
                sheet_physics.update('H8',T7['true_7'])
                sheet_physics.update('B8',T7['A'])
                sheet_physics.update('C8',T7['B'])
                sheet_physics.update('D8',T7['C'])
                sheet_physics.update('E8',T7['D'])
                sheet_physics.update('F8',T7['E'])
                sheet_physics.update('G8',T7['F'])
            if User_data['lesson']=="Информатика":#Обновление таблицы с задачами
                sheet_informatics.update('A8',T7['task_7'])
                sheet_informatics.update('B8',T7['true_7'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A8',T7['task_7'])
                sheet_medic.update('H8',T7['true_7'])
                sheet_medic.update('B8',T7['A'])
                sheet_medic.update('C8',T7['B'])
                sheet_medic.update('D8',T7['C'])
                sheet_medic.update('E8',T7['D'])
                sheet_medic.update('F8',T7['E'])
                sheet_medic.update('G8',T7['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A8',T7['task_7'])
                sheet_traffic.update('H8',T7['true_7'])
                sheet_traffic.update('B8',T7['A'])
                sheet_traffic.update('C8',T7['B'])
                sheet_traffic.update('D8',T7['C'])
                sheet_traffic.update('E8',T7['D'])
                sheet_traffic.update('F8',T7['E'])
                sheet_traffic.update('G8',T7['F'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 7 успешно обновлено', color="green")
    async def retask_8(): 	#Изменение 8-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №8\n'+str(L_sheet_math[8]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №8\n'+str(L_sheet_math_true[8]))#Текущий ответ задачи
            if User_data['lesson']=="Физика" or User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']== "Физика":
                    put_text('\nТекущие условие задачи №8\n'+str(L_sheet_physics[8]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №8\n'+str(L_sheet_physics_A[8])+'\n'+str(L_sheet_physics_B[8])+'\n'+str(L_sheet_physics_C[8])+'\n'+str(L_sheet_physics_D[8])+'\n'+str(L_sheet_physics_E[8])+'\n'+str(L_sheet_physics_F[8]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №8\n'+str(L_sheet_physics_true[8]))#Текущий ответ задачи
                elif User_data['lesson']== "Медицина":
                    put_text('\nТекущие условие задачи №8\n'+str(L_sheet_medic[8]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №8\n'+str(L_sheet_medic_A[8])+'\n'+str(L_sheet_medic_B[8])+'\n'+str(L_sheet_medic_C[8])+'\n'+str(L_sheet_medic_D[8])+'\n'+str(L_sheet_medic_E[8])+'\n'+str(L_sheet_medic_F[8]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №8\n'+str(L_sheet_medic_true[8]))#Текущий ответ задачи
                elif User_data['lesson']== "ПДД":
                    put_text('\nТекущие условие задачи №8\n'+str(L_sheet_traffic[8]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №8\n'+str(L_sheet_traffic_A[8])+'\n'+str(L_sheet_traffic_B[8])+'\n'+str(L_sheet_traffic_C[8])+'\n'+str(L_sheet_traffic_D[8])+'\n'+str(L_sheet_traffic_E[8])+'\n'+str(L_sheet_traffic_F[8]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №8\n'+str(L_sheet_traffic_true[8]))#Текущий ответ задачи
                T8=await input_group("", [
                input("Введите новое условие задачи №8", name='task_8'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №8", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №8", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №8", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №8", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №8", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №8", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №8", name='true_8'),#Ввод нового ответа для задачи
                ])

            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №8\n'+str(L_sheet_informatics[8]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №8\n'+str(L_sheet_informatics_true[8]))#Текущий ответ задачи

            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №8\n'+str(L_sheet_informatics[8]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №8\n'+str(L_sheet_informatics_true[8]))#Текущий ответ задачи

            if User_data['lesson']!="Физика" or User_data['lesson']!="Медицина" or User_data['lesson']!="ПДД":
                T8=await input_group("", [
                    input("Введите новое условие задачи №8", name='task_8'),#Ввод нового условия для задачи
                    input("Введите новый ответ задачи №8", name='true_8'),#Ввод нового ответа для задачи
                    ])
            if User_data['lesson']=="Математика":#Обновление таблицы с задачами
                sheet_math.update('A9',T8['task_8'])
                sheet_math.update('B9',T8['true_8'])
            if User_data['lesson']=="Физика":#Обновление таблицы с задачами
                sheet_physics.update('A9',T8['task_8'])
                sheet_physics.update('H9',T8['true_8'])
                sheet_physics.update('B9',T8['A'])
                sheet_physics.update('C9',T8['B'])
                sheet_physics.update('D9',T8['C'])
                sheet_physics.update('E9',T8['D'])
                sheet_physics.update('F9',T8['E'])
                sheet_physics.update('G9',T8['F'])
            if User_data['lesson']=="Информатика":#Обновление таблицы с задачами
                sheet_informatics.update('A9',T8['task_8'])
                sheet_informatics.update('B9',T8['true_8'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A9',T8['task_8'])
                sheet_medic.update('H9',T8['true_8'])
                sheet_medic.update('B9',T8['A'])
                sheet_medic.update('C9',T8['B'])
                sheet_medic.update('D9',T8['C'])
                sheet_medic.update('E9',T8['D'])
                sheet_medic.update('F9',T8['E'])
                sheet_medic.update('G9',T8['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A9',T8['task_8'])
                sheet_traffic.update('H9',T8['true_8'])
                sheet_traffic.update('B9',T8['A'])
                sheet_traffic.update('C9',T8['B'])
                sheet_traffic.update('D9',T8['C'])
                sheet_traffic.update('E9',T8['D'])
                sheet_traffic.update('F9',T8['E'])
                sheet_traffic.update('G9',T8['F'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 8 успешно обновлено', color="green")
    async def retask_9(): 	#Изменение 9-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №9\n'+str(L_sheet_math[9]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №9\n'+str(L_sheet_math_true[9]))#Текущий ответ задачи
            if User_data['lesson']=="Физика" or User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']== "Физика":
                    put_text('\nТекущие условие задачи №9\n'+str(L_sheet_physics[9]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №9\n'+str(L_sheet_physics_A[9])+'\n'+str(L_sheet_physics_B[9])+'\n'+str(L_sheet_physics_C[9])+'\n'+str(L_sheet_physics_D[9])+'\n'+str(L_sheet_physics_E[9])+'\n'+str(L_sheet_physics_F[9]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №9\n'+str(L_sheet_physics_true[9]))#Текущий ответ задачи
                elif User_data['lesson']== "Медицина":
                    put_text('\nТекущие условие задачи №9\n'+str(L_sheet_medic[9]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №9\n'+str(L_sheet_medic_A[9])+'\n'+str(L_sheet_medic_B[9])+'\n'+str(L_sheet_medic_C[9])+'\n'+str(L_sheet_medic_D[9])+'\n'+str(L_sheet_medic_E[9])+'\n'+str(L_sheet_medic_F[9]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №9\n'+str(L_sheet_medic_true[9]))#Текущий ответ задачи
                elif User_data['lesson']== "ПДД":
                    put_text('\nТекущие условие задачи №9\n'+str(L_sheet_traffic[9]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №9\n'+str(L_sheet_traffic_A[9])+'\n'+str(L_sheet_traffic_B[9])+'\n'+str(L_sheet_traffic_C[9])+'\n'+str(L_sheet_traffic_D[9])+'\n'+str(L_sheet_traffic_E[9])+'\n'+str(L_sheet_traffic_F[9]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №9\n'+str(L_sheet_traffic_true[9]))#Текущий ответ задачи
                T9=await input_group("", [
                input("Введите новое условие задачи №9", name='task_9'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №9", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №9", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №9", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №9", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №9", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №9", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №9", name='true_9'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №9\n'+str(L_sheet_informatics[9]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №9\n'+str(L_sheet_informatics_true[9]))#Текущий ответ задачи
            if User_data['lesson']!="Физика" or User_data['lesson']!="Медицина" or User_data['lesson']!="ПДД":
                T9=await input_group("", [
                    input("Введите новое условие задачи №9", name='task_9'),#Ввод нового условия для задачи#Ввод нового условия для задачи
                    input("Введите новый ответ задачи №9", name='true_9'),#Ввод нового ответа для задачи
                    ])
            if User_data['lesson']=="Математика":#Обновление таблицы с задачами
                sheet_math.update('A10',T9['task_9'])
                sheet_math.update('B10',T9['true_9'])
            if User_data['lesson']=="Физика":#Обновление таблицы с задачами
                sheet_physics.update('A10',T9['task_9'])
                sheet_physics.update('H10',T9['true_9'])
                sheet_physics.update('B10',T9['A'])
                sheet_physics.update('C10',T9['B'])
                sheet_physics.update('D10',T9['C'])
                sheet_physics.update('E10',T9['D'])
                sheet_physics.update('F10',T9['E'])
                sheet_physics.update('G10',T9['F'])
            if User_data['lesson']=="Информатика":#Обновление таблицы с задачами
                sheet_informatics.update('A10',T9['task_9'])
                sheet_informatics.update('B10',T9['true_9'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A10',T9['task_9'])
                sheet_medic.update('H10',T9['true_9'])
                sheet_medic.update('B10',T9['A'])
                sheet_medic.update('C10',T9['B'])
                sheet_medic.update('D10',T9['C'])
                sheet_medic.update('E10',T9['D'])
                sheet_medic.update('F10',T9['E'])
                sheet_medic.update('G10',T9['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A10',T9['task_9'])
                sheet_traffic.update('H10',T9['true_9'])
                sheet_traffic.update('B10',T9['A'])
                sheet_traffic.update('C10',T9['B'])
                sheet_traffic.update('D10',T9['C'])
                sheet_traffic.update('E10',T9['D'])
                sheet_traffic.update('F10',T9['E'])
                sheet_traffic.update('G10',T9['F'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 9 успешно обновлено', color="green")
    async def retask_10(): 	#Изменение 10-го задания
        with use_scope('scope_2', clear=True):
            if User_data['lesson']=="Математика":
                put_text('\nТекущие условие задачи №10\n'+str(L_sheet_math[10]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №10\n'+str(L_sheet_math_true[10]))#Текущий ответ задачи
            if User_data['lesson']=="Физика" or User_data['lesson']=="Медицина" or User_data['lesson']=="ПДД":
                if User_data['lesson']== "Физика":
                    put_text('\nТекущие условие задачи №10\n'+str(L_sheet_physics[10]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №10\n'+str(L_sheet_physics_A[10])+'\n'+str(L_sheet_physics_B[10])+'\n'+str(L_sheet_physics_C[10])+'\n'+str(L_sheet_physics_D[10])+'\n'+str(L_sheet_physics_E[10])+'\n'+str(L_sheet_physics_F[10]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №10\n'+str(L_sheet_physics_true[10]))#Текущий ответ задачи
                elif User_data['lesson']== "Медицина":
                    put_text('\nТекущие условие задачи №10\n'+str(L_sheet_medic[10]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №10\n'+str(L_sheet_medic_A[10])+'\n'+str(L_sheet_medic_B[10])+'\n'+str(L_sheet_medic_C[10])+'\n'+str(L_sheet_medic_D[10])+'\n'+str(L_sheet_medic_E[10])+'\n'+str(L_sheet_medic_F[10]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №10\n'+str(L_sheet_medic_true[10]))#Текущий ответ задачи
                elif User_data['lesson']== "ПДД":
                    put_text('\nТекущие условие задачи №10\n'+str(L_sheet_traffic[10]))#Текущие условие задачи
                    put_text('\nТекущий варианты к задаче №10\n'+str(L_sheet_traffic_A[10])+'\n'+str(L_sheet_traffic_B[10])+'\n'+str(L_sheet_traffic_C[10])+'\n'+str(L_sheet_traffic_D[10])+'\n'+str(L_sheet_traffic_E[10])+'\n'+str(L_sheet_traffic_F[10]))#Текущий варианты к задаче
                    put_text('\nТекущий правильный ответ к задаче №10\n'+str(L_sheet_traffic_true[10]))#Текущий ответ задачи
                T10=await input_group("", [
                input("Введите новое условие задачи №10", name='task_10'),#Ввод нового условия для задачи
                input("Введите новый вариант А ответа к задаче №10", name='A'),#Ввод варианта ответа А
                input("Введите новый вариант Б ответа к задаче №10", name='B'),#Ввод варианта ответа Б
                input("Введите новый вариант В ответа к задаче №10", name='C'),#Ввод варианта ответа В
                input("Введите новый вариант Г ответа к задаче №10", name='D'),#Ввод варианта ответа Г
                input("Введите новый вариант Д ответа к задаче №10", name='E'),#Ввод варианта ответа Д
                input("Введите новый вариант Е ответа к задаче №10", name='F'),#Ввод варианта ответа Е
                input("Введите новый правильный ответ к задаче №10", name='true_10'),#Ввод нового ответа для задачи
                ])
            if User_data['lesson']=="Информатика":
                put_text('\nТекущие условие задачи №10\n'+str(L_sheet_informatics[10]))#Текущие условие задачи
                put_text('\nТекущий ответ к задаче №10\n'+str(L_sheet_informatics_true[10]))#Текущий ответ задачи
            if User_data['lesson']!="Физика" or User_data['lesson']!="Медицина" or User_data['lesson']!="ПДД":
                T10=await input_group("", [
                    input("Введите новое условие задачи №10", name='task_10'),#Ввод нового условия для задачи
                    input("Введите новый ответ задачи №10", name='true_10'),#Ввод нового ответа для задачи
                    ])
            if User_data['lesson']=="Математика":#Обновление таблицы с задачами
                sheet_math.update('A11',T10['task_10'])
                sheet_math.update('B11',T10['true_10'])
            if User_data['lesson']=="Физика":#Обновление таблицы с задачами
                sheet_physics.update('A11',T10['task_10'])
                sheet_physics.update('H11',T10['true_10'])
                sheet_physics.update('B11',T10['A'])
                sheet_physics.update('C11',T10['B'])
                sheet_physics.update('D11',T10['C'])
                sheet_physics.update('E11',T10['D'])
                sheet_physics.update('F11',T10['E'])
                sheet_physics.update('G11',T10['F'])
            if User_data['lesson']=="Информатика":#Обновление таблицы с задачами
                sheet_informatics.update('A11',T10['task_10'])
                sheet_informatics.update('B11',T10['true_10'])
            if User_data['lesson']=="Медицина":           #Обновление таблицы с задачами
                sheet_medic.update('A11',T10['task_10'])
                sheet_medic.update('H11',T10['true_10'])
                sheet_medic.update('B11',T10['A'])
                sheet_medic.update('C11',T10['B'])
                sheet_medic.update('D11',T10['C'])
                sheet_medic.update('E11',T10['D'])
                sheet_medic.update('F11',T10['E'])
                sheet_medic.update('G11',T10['F'])
            if User_data['lesson']=="ПДД":           #Обновление таблицы с задачами
                sheet_traffic.update('A11',T10['task_10'])
                sheet_traffic.update('H11',T10['true_10'])
                sheet_traffic.update('B11',T10['A'])
                sheet_traffic.update('C11',T10['B'])
                sheet_traffic.update('D11',T10['C'])
                sheet_traffic.update('E11',T10['D'])
                sheet_traffic.update('F11',T10['E'])
                sheet_traffic.update('G11',T10['F'])
            with use_scope('scope_2', clear=True):
                put_text('')
            toast('Задание 10 успешно обновлено', color="green")

    #async def check_full_answer(): #Проверка пояснений к ответам
        #with use_scope('scope_4',clear=True):
            #toast('Проверка закончена', color="green")

    with use_scope('scope_1', clear=True):
        put_markdown("## 🧊 Это панель администатора\n").style('color: black; font-size: 50px, text-align:left')

        put_table([ #кнопки для запуска функций изменения заданий
            [put_button(['Задание 01'], onclick=retask_1),put_button(['Задание 02'], onclick=retask_2),put_button(['Задание 03'], onclick=retask_3),put_button(['Задание 04'], onclick=retask_4),put_button(['Задание 05'], onclick=retask_5)],
            [put_button(['Задание 06'], onclick=retask_6),put_button(['Задание 07'], onclick=retask_7),put_button(['Задание 08'], onclick=retask_8),put_button(['Задание 09'], onclick=retask_9),put_button(['Задание 10'], onclick=retask_10)],
            ])
        put_text('\n')
        put_text('\npayment_to_programmers=["17000", "15000", "16500"]')
        put_table([         #разработчики
            ['Разработчики','Сколько им заплатили'],
            ['Кубашев Руслан','payment_to_programmers[0]'],
            ['Пахалев Алексей','payment_to_programmers[1]'],
            ['Фролкова Дарья','len(payment_to_programmers)']
            ])
        put_text('\n')
        put_button(['Изменить адрес почты'], onclick=change_mail)#кнопка для запуска функции изменения почты
        #put_button(['Начать проверку полных ответов'], onclick=check_full_answer)#кнопка для запуска функции проверки полных ответов
        put_button(['Вернуться на главную'], onclick=main)#кнопка для возвращения на главную страницу

async def test(): #Тестирование
    global true_list, false_list, scores, msg, recipient_mail, L_sheet_math, L_sheet_physics, L_sheet_informatics, L_sheet_mails, math_mail, physics_mail, informatics_mail, L_sheet_math_full_answers, L_sheet_informatics_full_answers, L_sheet_physics_full_answers
    with use_scope('scope_1', clear=True):
        put_markdown("## 🧊 Загрузка таблиц\n").style('color: black; font-size: 50px,text-align:left') #загрузка и открытие таблиц
        put_processbar('bar');
        i=1
        set_processbar('bar', i / 5)

    if User_data['lesson']=='Математика':
        if User_data['class']=='8':
            sheet_math=client.open('math_8').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.get_all_records()       #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
            i+=1
            set_processbar('bar', i / 5)
        elif User_data['class']=='7':
            sheet_math=client.open('math_7').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.get_all_records()       #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
            i+=1
            set_processbar('bar', i / 5)
        elif User_data['class']=='6':
            sheet_math=client.open('math_6').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.get_all_records()       #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
            i+=1
            set_processbar('bar', i / 5)
        elif User_data['class']=='5':
            sheet_math=client.open('math_5').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.get_all_records()       #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
            i+=1
            set_processbar('bar', i / 5)
        else:
            sheet_math=client.open('math_tasks').sheet1     #Подключение к таблице с заданиями тестирования по математике
            L_sheet_math=sheet_math.get_all_records()       #Создание локальной переменной с заданиями тестирования по математике
            L_sheet_math_true=sheet_math.col_values(2)      #Создание локальной переменной с ответами тестирования по математике
            i+=1
            set_processbar('bar', i / 5)
            #sheet_humans_math=client.open('humans_math').sheet1         #Подключение к таблице с людьми, прошедших тестирование по математике
            #L_sheet_humans_math=sheet_humans_math.get_all_records()     #Создание локальной переменной с людьми, прошедших тестирование по математике
            i+=1
            set_processbar('bar', i / 5)
            #sheet_math_full_answers=client.open('math_full_answers').sheet1         #Подключение к таблице с пояснениями к ответам пользователей, прошедших тестирование по математике
            #L_sheet_math_full_answers=sheet_math_full_answers.get_all_records()     #Создание локальной переменной с пояснениями к ответам пользователей, прошедших тестирование по математике
            i+=1
            set_processbar('bar', i / 5)
            recipient_mail=sheet_mails.cell(2,2).value  #Выбор нужной почты для отправки письма
            i+=1
            set_processbar('bar', i / 5)

    if User_data['lesson']=='Информатика':
        sheet_informatics=client.open('informatics_tasks').sheet1       #Подключение к таблице с заданиями тестирования по информатике
        L_sheet_informatics=sheet_informatics.get_all_records()         #Создание локальной переменной с заданиями тестирования по информатике
        L_sheet_informatics_true=sheet_informatics.col_values(2)        #Создание локальной переменной с ответами тестирования по информатике
        i+=1
        set_processbar('bar', i / 5)
        #sheet_humans_informatics=client.open('humans_inform').sheet1    #Подключение к таблице с людьми, прошедших тестирование по информатике
        #L_sheet_humans_informatics=sheet_humans_informatics.get_all_records() #Создание локальной переменной с людьми, прошедших тестирование по информатике
        i+=1
        set_processbar('bar', i / 5)
        #sheet_informatics_full_answers=client.open('informatics_full_answers').sheet1   #Подключение к таблице с пояснениями к ответам пользователей, прошедших тестирование по информатике
        #L_sheet_informatics_full_answers=sheet_informatics_full_answers.get_all_records()  #Создание локальной переменной с людьми, прошедших тестирование по информатике
        i+=1
        set_processbar('bar', i / 5)
        recipient_mail=sheet_mails.cell(4,2).value #Выбор нужной почты для отправки письма
        i+=1
        set_processbar('bar', i / 5)

    if User_data['lesson']=='Физика':
        sheet_physics=client.open('physics_tasks').sheet1       #Подключение к таблице с заданиями тестирования по физике
        L_sheet_physics=sheet_physics.get_all_records()         #Создание локальной переменной с заданиями тестирования по физике
        i+=1
        set_processbar('bar', i / 5)
        #sheet_humans_physics=client.open('humans_physics').sheet1   #Подключение к таблице с людьми, прошедших тестирование по физике
        #L_sheet_humans_physics=sheet_humans_physics.get_all_records() #Создание локальной переменной с людьми, прошедших тестирование по физике
        i+=1
        set_processbar('bar', i / 5)
        #sheet_physics_full_answers=client.open('physics_full_answers').sheet1   #Подключение к таблице с пояснениями к ответам пользователей, прошедших тестирование по физике
        #L_sheet_physics_full_answers=sheet_physics_full_answers.get_all_records()  #Создание локальной переменной с людьми, прошедших тестирование по физике
        i+=1
        set_processbar('bar', i / 5)
        recipient_mail=sheet_mails.cell(3,2).value      #Выбор нужной почты для отправки письма
        i+=1
        set_processbar('bar', i / 5)

    if User_data['lesson']=='Медицина': 
        ran=int(random.randint(1,3))
        i+=1
        set_processbar('bar', i / 2)
        if ran == 1 : 
            sheet_physics = client.open('Medic_1').sheet1                         #Подключение к таблице с заданиями тестирования по медицине
        if ran == 2 : 
            sheet_physics = client.open('Medic_2').sheet1                         #Подключение к таблице с заданиями тестирования по медицине
        if ran == 3 : 
            sheet_physics = client.open('Medic_3').sheet1                         #Подключение к таблице с заданиями тестирования по медицине
        L_sheet_physics = sheet_physics.get_all_records()                         #Создание локальной переменной с заданиями тестирования по медицине

        recipient_mail=sheet_mails.cell(5,2).value      #Выбор нужной почты для отправки письма
        i+=1
        set_processbar('bar', i / 5)

    if User_data['lesson']=='ПДД':
        ran=int(random.randint(1,2))
        i+=1
        set_processbar('bar', i / 2)
        if ran==1:
            sheet_physics = client.open('traffic_rules_1').sheet1 
        elif ran==2:                            #Подключение к таблице с заданиями тестирования по ПДД
            sheet_physics = client.open('traffic_rules_2').sheet1 
        L_sheet_physics=sheet_physics.get_all_records()                                 #Создание локальной переменной с заданиями тестирования по ПДД
        i+=1
        set_processbar('bar', i / 5)
        recipient_mail=sheet_mails.cell(5,2).value      #Выбор нужной почты для отправки письма
        i+=1
        set_processbar('bar', i / 5)

    true_list=[] 	#Список верновыполненных заданий
    false_list=[]	#Список неверновыполненных заданий

    async def task_1():  #1 задание
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 1 Задание\n").style('color: black; font-size: 50px,text-align:left')

            if User_data['lesson']=='Математика':
                task_1=str(L_sheet_math[0]).partition("'условие': '")[2].partition("', 'ответ")[0]  #Условие
                User_answers_1=await input_group('',[                                               #Ответ на задание
                    input(task_1, name='answer_1'), 
                    #textarea(label='Пояснение: ', rows=10, name='full_task_1')  #Пояснение
                    ])
                if User_answers_1['answer_1'].lower()==str(L_sheet_math_true[1]):                   #Проверка ответа
                    true_list.append('1')                                                           #Добавление в список верновыполненных заданий
                else: false_list.append('1')                                                        #Добавление в список неверновыполненных заданий

            elif User_data['lesson']=='Физика':
                task_1=str(L_sheet_physics[0]).partition("'условие': '")[2].partition("', 'А'")[0]  #Условие
                User_answers_1=await checkbox(task_1, [str(L_sheet_physics[0]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[0]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[0]).partition("'В': '")[2].partition("', 'Г'")[0], str(L_sheet_physics[0]).partition("'Г': '")[2].partition("', 'Д'")[0], str(L_sheet_physics[0]).partition("'Д': '")[2].partition("', 'Е'")[0], str(L_sheet_physics[0]).partition("'Е': '")[2].partition("', 'Правильный ответ'")[0] ])#кнопки для ответа на задание
                A_B_C=str(User_answers_1).split('.')
                A=str(A_B_C[0]).partition("'")[2].partition(".")[0]
                B=str(A_B_C[1]).partition(" '")[2].partition(".")[0]
                C=str(A_B_C[2]).partition(" '")[2].partition(".")[0]
                if A in str(sheet_physics.cell(2,8).value) and B in str(sheet_physics.cell(2,8).value) and C in str(sheet_physics.cell(2,8).value):#Проверка ответа
                    true_list.append('1')                                                           #Добавление в список верновыполненных заданий
                else: false_list.append('1')                                                        #Добавление в список неверновыполненных заданий

            elif User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                if User_data['lesson']=='Медицина':
                    toast("На выполнение работы вам отводиться 20 минут", color="green")
                task_1=str(L_sheet_physics[0]).partition("'условие': '")[2].partition("', 'А'")[0]           
                if User_data['lesson']=='ПДД':
                    if ran==2:
                        img_1 = open('ПДД/1,1.png', 'rb').read()  
                        put_image(img_1, width='700px').style('text-align: center')
                User_answers_1=await radio(task_1, [str(L_sheet_physics[0]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[0]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[0]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                if str(L_sheet_physics[0]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_1).partition(". ")[0]:  #Проверка ответа
                    true_list.append('1')                                                                     #Добавление в список верновыполненных заданий
                else: false_list.append('1')                                                                 

            elif User_data['lesson']=='Информатика':
                task_1=str(L_sheet_informatics[0]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                User_answers_1=await input_group('', [
                    input(task_1, name='answer_1'),#ответ на задание
                    #textarea(label='Пояснение: ', rows=10, name='full_task_1')#пояснение
                    ])
                if User_answers_1['answer_1'].lower()==str(L_sheet_informatics_true[1]):#Проверка ответа
                    true_list.append('1')#добовление в список верновыполненных заданий
                else: false_list.append('1')#добовление в список неверновыполненных заданий

            with use_scope('scope_1', clear=True):
                put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError: #действие при большой нагрузке
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_1()

    async def task_2():  #2 задание
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 2 Задание\n").style('color: black; font-size: 50px,text-align:left')

                if User_data['lesson']=='Математика':
                    task_2=str(L_sheet_math[1]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_2=await input_group('', [
                        input(task_2, name='answer_2'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_2')#пояснение
                        ])
                    if User_answers_2['answer_2'].lower()==str(L_sheet_math_true[2]):#Проверка ответа
                        true_list.append('2')#добовление в список верновыполненных заданий
                    else: false_list.append('2')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Физика' or  User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                    task_2=str(L_sheet_physics[1]).partition("'условие': '")[2].partition("', 'А'")[0]#условие
                    if User_data['lesson']=='ПДД':
                        if ran==1:
                            img_2 = open('ПДД/2.png', 'rb').read()  
                            put_image(img_2, width='700px').style('text-align: center')
                        if ran==2:
                            img_2 = open('ПДД/1,2.png', 'rb').read()  
                            put_image(img_2, width='500px').style('text-align: center')
                    User_answers_2=await radio(task_2, [str(L_sheet_physics[1]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[1]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[1]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                    if str(L_sheet_physics[1]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_2).partition(". ")[0]:  #Проверка ответа
                        true_list.append('2')                                                                     #Добавление в список верновыполненных заданий
                    else: false_list.append('2')                                                                  #Добавление в список неверновыполненных заданий

                elif User_data['lesson']=='Информатика':
                    task_2=str(L_sheet_informatics[1]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_2=await input_group('', [
                        input(task_2, name='answer_2'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_2')#пояснение
                        ])
                    if User_answers_2['answer_2'].lower()==str(L_sheet_informatics_true[2]):#Проверка ответа
                        true_list.append('2')#добовление в список верновыполненных заданий
                    else: false_list.append('2')#добовление в список неверновыполненных заданий

                with use_scope('scope_1', clear=True):
                        put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError:#действие при большой нагрузке
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_2()

    async def task_3():  #3 задание
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 3 Задание\n").style('color: black; font-size: 50px,text-align:left')
                if User_data['lesson']=='Математика':
                    task_3=str(L_sheet_math[2]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_3=await input_group('', [
                        input(task_3, name='answer_3'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_3')#пояснение
                        ])
                    if User_answers_3['answer_3'].lower()==str(L_sheet_math_true[3]):#Проверка ответа
                        true_list.append('3')#добовление в список верновыполненных заданий
                    else: false_list.append('3')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Физика' or  User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                    task_3=str(L_sheet_physics[2]).partition("'условие': '")[2].partition("', 'А'")[0]#условие
                    if User_data['lesson']=='ПДД':
                        if ran==1:
                            img_3 = open('ПДД/3.png', 'rb').read()  
                            put_image(img_3, width='700px').style('text-align: center')
                        if ran==2:
                            img_3 = open('ПДД/1,3.png', 'rb').read()  
                            put_image(img_3, width='500px').style('text-align: center')
                    User_answers_3=await radio(task_3, [str(L_sheet_physics[2]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[2]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[2]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                    if str(L_sheet_physics[2]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_3).partition(". ")[0]:  #Проверка ответа #Проверка ответа
                        true_list.append('3')                                                                     #Добавление в список верновыполненных заданий
                    else: false_list.append('3')

                elif User_data['lesson']=='Информатика':
                    task_3=str(L_sheet_informatics[2]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_3=await input_group('', [
                        input(task_3, name='answer_3'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_3')#пояснение
                        ])
                    if User_answers_3['answer_3'].lower()==str(L_sheet_informatics_true[3]):#Проверка ответа
                        true_list.append('3')#добовление в список верновыполненных заданий
                    else: false_list.append('3')#добовление в список неверновыполненных заданий

                with use_scope('scope_1', clear=True):
                        put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError:#действие при большой нагрузке
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_3()

    async def task_4():  #4 задание
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 4 Задание\n").style('color: black; font-size: 50px,text-align:left')
                if User_data['lesson']=='Математика':
                    task_4=str(L_sheet_math[3]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_4=await input_group('', [
                        input(task_4, name='answer_4'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_4')#пояснение
                        ])
                    if User_answers_4['answer_4'].lower()==str(L_sheet_math_true[4]):#Проверка ответа
                        true_list.append('4')#добовление в список верновыполненных заданий
                    else: false_list.append('4')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Физика' or  User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                    task_4=str(L_sheet_physics[3]).partition("'условие': '")[2].partition("', 'А'")[0]#условие
                    if User_data['lesson']=='ПДД':
                        if ran==2:
                            img_4 = open('ПДД/1,4.png', 'rb').read()  
                            put_image(img_4, width='500px').style('text-align: center')
                    User_answers_4=await radio(task_4, [str(L_sheet_physics[3]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[3]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[3]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                    if str(L_sheet_physics[3]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_4).partition(". ")[0]:  #Проверка ответа #Проверка ответа
                        true_list.append('4')#добовление в список верновыполненных заданий
                    else: false_list.append('4')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Информатика':
                    task_4=str(L_sheet_informatics[3]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_4=await input_group('', [
                        input(task_4, name='answer_4'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_4')#пояснение
                        ])
                    if User_answers_4['answer_4'].lower()==str(L_sheet_informatics_true[4]):#Проверка ответа
                        true_list.append('4')#добовление в список верновыполненных заданий
                    else: false_list.append('4')#добовление в список неверновыполненных заданий

                with use_scope('scope_1', clear=True):
                        put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError:#действие при большой нагрузке
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_4()

    async def task_5():  #5 задание
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 5 Задание\n").style('color: black; font-size: 50px,text-align:left')
                if User_data['lesson']=='Математика':
                    task_5=str(L_sheet_math[4]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_5=await input_group('', [
                        input(task_5, name='answer_5'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_5')#пояснение
                        ])
                    if User_answers_5['answer_5'].lower()==str(L_sheet_math_true[5]):#Проверка ответа
                        true_list.append('5')#добовление в список верновыполненных заданий
                    else: false_list.append('5')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Физика' or  User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                    task_5=str(L_sheet_physics[4]).partition("'условие': '")[2].partition("', 'А'")[0]  #условие
                    if User_data['lesson']=='ПДД':
                        if ran==2:
                            img_5 = open('ПДД/1,5.png', 'rb').read()  
                            put_image(img_5, width='500px').style('text-align: center')
                    User_answers_5=await radio(task_5, [str(L_sheet_physics[4]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[4]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[4]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                    if str(L_sheet_physics[4]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_5).partition(". ")[0]:  #Проверка ответа 
                        true_list.append('5')#добовление в список верновыполненных заданий
                    else: false_list.append('5')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Информатика':
                    task_5=str(L_sheet_informatics[4]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_5=await input_group('', [
                        input(task_5, name='answer_5'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_5')#пояснение
                        ])
                    if User_answers_5['answer_5'].lower()==str(L_sheet_informatics_true[5]):#Проверка ответа
                        true_list.append('5')#добовление в список верновыполненных заданий
                    else: false_list.append('5')#добовление в список неверновыполненных заданий

                with use_scope('scope_1', clear=True):
                        put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError:#действие при большой нагрузке
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_5()

    async def task_6():  #6 задание
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 6 Задание\n").style('color: black; font-size: 50px,text-align:left')
                if User_data['lesson']=='Математика':
                    task_6=str(L_sheet_math[5]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_6=await input_group('', [
                        input(task_6, name='answer_6'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_6')#пояснение
                        ])
                    if User_answers_6['answer_6'].lower()==str(L_sheet_math_true[6]):#Проверка ответа
                        true_list.append('6')#добовление в список верновыполненных заданий
                    else: false_list.append('6')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Физика' or  User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                    task_6=str(L_sheet_physics[5]).partition("'условие': '")[2].partition("', 'А'")[0]#условие
                    if User_data['lesson']=='ПДД':
                        if ran==2:
                            img_6 = open('ПДД/1,6.png', 'rb').read()  
                            put_image(img_6, width='500px').style('text-align: center')
                    User_answers_6=await radio(task_6, [str(L_sheet_physics[5]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[5]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[5]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                    if str(L_sheet_physics[5]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_6).partition(". ")[0]:  #Проверка ответа #Проверка ответа
                        true_list.append('6')#добовление в список верновыполненных заданий
                    else: false_list.append('6')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Информатика':
                    task_6=str(L_sheet_informatics[5]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_6=await input_group('', [
                        input(task_6, name='answer_6'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_6')#пояснение
                        ])
                    if User_answers_6['answer_6'].lower()==str(L_sheet_informatics_true[6]):#Проверка ответа
                        true_list.append('6')#добовление в список верновыполненных заданий
                    else: false_list.append('6')#добовление в список неверновыполненных заданий

                with use_scope('scope_1', clear=True):
                        put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError:#действие при большой нагрузке
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_6()

    async def task_7():  #7 задание
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 7 Задание\n").style('color: black; font-size: 50px,text-align:left')
                if User_data['lesson']=='Математика':
                    task_7=str(L_sheet_math[6]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_7=await input_group('', [
                        input(task_7, name='answer_7'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_7')#пояснение
                        ])
                    if User_answers_7['answer_7'].lower()==str(L_sheet_math_true[7]):#Проверка ответа
                        true_list.append('7')#добовление в список верновыполненных заданий
                    else: false_list.append('7')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Физика' or  User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                    task_7=str(L_sheet_physics[6]).partition("'условие': '")[2].partition("', 'А'")[0]#условие
                    if User_data['lesson']=='ПДД':
                        if ran==2:
                            img_7 = open('ПДД/1,7.png', 'rb').read()  
                            put_image(img_7, width='700px').style('text-align: center')
                    User_answers_7=await radio(task_7, [str(L_sheet_physics[6]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[6]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[6]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                    if str(L_sheet_physics[6]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_7).partition(". ")[0]:  #Проверка ответа #Проверка ответа
                        true_list.append('7')#добовление в список верновыполненных заданий
                    else: false_list.append('7')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Информатика':
                    task_7=str(L_sheet_informatics[6]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_7=await input_group('', [
                        input(task_7, name='answer_7'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_7')#пояснение
                        ])
                    if User_answers_7['answer_7'].lower()==str(L_sheet_informatics_true[7]):#Проверка ответа
                        true_list.append('7')#добовление в список верновыполненных заданий
                    else: false_list.append('7')#добовление в список неверновыполненных заданий

                with use_scope('scope_1', clear=True):
                        put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError:#действие при большой нагрузке
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_7()

    async def task_8():  #8 задание
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 8 Задание\n").style('color: black; font-size: 50px,text-align:left')
                if User_data['lesson']=='Математика':
                    task_8=str(L_sheet_math[7]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_8=await input_group('', [
                        input(task_8, name='answer_8'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_8')#пояснение
                        ])
                    if User_answers_8['answer_8'].lower()==str(L_sheet_math_true[8]):#Проверка ответа
                        true_list.append('8')#добовление в список верновыполненных заданий
                    else: false_list.append('8')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Физика' or  User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                    task_8=str(L_sheet_physics[7]).partition("'условие': '")[2].partition("', 'А'")[0]#условие
                    if User_data['lesson']=='ПДД':
                        if ran==2:
                            img_8 = open('ПДД/1,8.png', 'rb').read()  
                            put_image(img_8, width='500px').style('text-align: center')
                    User_answers_8=await radio(task_8, [str(L_sheet_physics[7]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[7]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[7]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                    if str(L_sheet_physics[7]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_8).partition(". ")[0]:  #Проверка ответа 
                        true_list.append('8')#добовление в список верновыполненных заданий
                    else: false_list.append('8')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Информатика':
                    task_8=str(L_sheet_informatics[7]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_8=await input_group('', [
                        input(task_8, name='answer_8'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_8')#пояснение
                        ])
                    if User_answers_8['answer_8'].lower()==str(L_sheet_informatics_true[8]):#Проверка ответа
                        true_list.append('8')#добовление в список верновыполненных заданий
                    else: false_list.append('8')#добовление в список неверновыполненных заданий

                with use_scope('scope_1', clear=True):
                        put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError:#действие при большой нагрузке
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_8()

    async def task_9():  #9 задание#
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 9 Задание\n").style('color: black; font-size: 50px,text-align:left')
                if User_data['lesson']=='Математика':
                    task_9=str(L_sheet_math[8]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_9=await input_group('', [
                        input(task_9, name='answer_9'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_9')#пояснение
                        ])
                    if User_answers_9['answer_9'].lower()==str(L_sheet_math_true[9]):#Проверка ответа
                        true_list.append('9')#добовление в список верновыполненных заданий
                    else: false_list.append('9')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Физика' or  User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                    task_9=str(L_sheet_physics[8]).partition("'условие': '")[2].partition("', 'А'")[0]#условие
                    if User_data['lesson']=='ПДД':
                        if ran==2:
                            img_9 = open('ПДД/1,9.png', 'rb').read()  
                            put_image(img_9, width='500px').style('text-align: center')
                    User_answers_9=await radio(task_9, [str(L_sheet_physics[8]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[8]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[8]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                    if str(L_sheet_physics[8]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_9).partition(". ")[0]:   #Проверка ответа
                        true_list.append('9')#добовление в список верновыполненных заданий
                    else: false_list.append('9')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Информатика':
                    task_9=str(L_sheet_informatics[8]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_9=await input_group('', [
                        input(task_9, name='answer_9'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_9')#пояснение
                        ])
                    if User_answers_9['answer_9'].lower()==str(L_sheet_informatics_true[9]):#Проверка ответа
                        true_list.append('9')#добовление в список верновыполненных заданий
                    else: false_list.append('9')#добовление в список неверновыполненных заданий

                with use_scope('scope_1', clear=True):
                        put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError:#действие при большой нагрузке
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_9()

    async def task_10(): #10 задание
        try:
            with use_scope('scope_1', clear=True):
                put_markdown("## 🧊 10 Задание\n").style('color: black; font-size: 50px,text-align:left')
                if User_data['lesson']=='Математика':
                    task_10=str(L_sheet_math[9]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_10=await input_group('', [
                        input(task_10, name='answer_10'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_10')#пояснение
                        ])
                    if User_answers_10['answer_10'].lower()==str(L_sheet_math_true[10]):#Проверка ответа
                        true_list.append('10')#добовление в список верновыполненных заданий
                    else: false_list.append('10')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Физика' or  User_data['lesson']=='Медицина' or User_data['lesson']=='ПДД':
                    task_10=str(L_sheet_physics[9]).partition("'условие': '")[2].partition("', 'А'")[0]#условие
                    if User_data['lesson']=='ПДД':
                        if ran==2:
                            img_10 = open('ПДД/1,10.png', 'rb').read()  
                            put_image(img_10, width='500px').style('text-align: center')
                    User_answers_10=await radio(task_10, [str(L_sheet_physics[9]).partition("'А': '")[2].partition("', 'Б'")[0], str(L_sheet_physics[9]).partition("'Б': '")[2].partition("', 'В'")[0], str(L_sheet_physics[9]).partition("'В': '")[2].partition("', 'Г'")[0] ])
                    if str(L_sheet_physics[9]).partition("'Правильный ответ': '")[2].partition("'")[0] == str(User_answers_10).partition(". ")[0]:  #Проверка ответа 
                        true_list.append("10")
                    else: 
                        false_list.append('10')#добовление в список неверновыполненных заданий

                elif User_data['lesson']=='Информатика':
                    task_10=str(L_sheet_informatics[9]).partition("'условие': '")[2].partition("', 'ответ")[0]#условие
                    User_answers_10=await input_group('', [
                        input(task_10, name='answer_10'),#ответ на задание
                        #textarea(label='Пояснение: ', rows=10, name='full_task_10')#пояснение
                        ])
                    if User_answers_10['answer_10'].lower()==str(L_sheet_informatics_true[10]):#Проверка ответа
                        true_list.append('10')#добовление в список верновыполненных заданий
                    else: false_list.append('10')#добовление в список неверновыполненных заданий

                with use_scope('scope_1', clear=True):
                        put_loading(shape='border', color='primary')

        except gspread.exceptions.APIError:
            toast("Большая нагрузка на сервер, пожалуйста, подождите!", color="red")
            time.sleep(15)
            await task_10()

    await task_1()  #Запуск функции с заданием
    await task_2()  #Запуск функции с заданием
    await task_3()  #Запуск функции с заданием
    await task_4()  #Запуск функции с заданием
    await task_5()  #Запуск функции с заданием
    await task_6()  #Запуск функции с заданием
    await task_7()  #Запуск функции с заданием
    await task_8()  #Запуск функции с заданием
    await task_9()  #Запуск функции с заданием
    await task_10() #Запуск функции с заданием

    scores = len(true_list)*10  #Кол-во баллов

    await send_results()

    with use_scope('scope_1', clear=True):
        put_markdown("## 🧊 Вы завершили тестирование!\n").style('color: black; font-size: 50px,text-align:left')

    if len(true_list)>=9: #Текст при 9 и более правильных ответов
        if User_data['gender']=='Мужской':
            put_text("\nМолодец, ты хорошо усвоил эту тему!\n").style('font-size: 20px; font-style: italic')
            if len(false_list)>0:
                put_text('Поработай над задачей номер : '+', '.join([str(i) for i in false_list])).style('font-size: 20px; font-style: italic') #Вывод не правильно решенных задач
            else:
                put_text('Поздравляем,у тебя нет ошибок').style('font-size: 20px; font-style: italic')
        else:
            put_text("\nМолодец, ты хорошо усвоила эту тему!\n").style('font-size: 20px; font-style: italic')
            if len(false_list)>0:
                put_text('Поработай над задачами номер : '+', '.join([str(i) for i in false_list])).style('font-size: 20px; font-style: italic')#Вывод не правильно решенных задач
            else:
                put_text('Поздравляем,у тебя нет ошибок').style('font-size: 20px; font-style: italic')
    elif len(true_list)>=7:#Текст при 7 и более правильных ответов
        put_text('\nХорошо, но есть небольшие недочёты\n').style('font-size: 20px; font-style: italic')
        put_text('Поработай над задачами номер : '+', '.join([str(i) for i in false_list])).style('font-size: 20px; font-style: italic')#Вывод не правильно решенных задач
    elif len(true_list)>=5:#Текст при 5 и более правильных ответов
        put_text('\nУверен, ты можешь лучше\n').style('font-size: 20px; font-style: italic')
        put_text('Поработай над задачами номер : '+', '.join([str(i) for i in false_list])).style('font-size: 20px; font-style: italic')#Вывод не правильно решенных задач
    elif len(true_list)<4:#Текст при 4 и менее правильных ответов
        if post=="teacher":
            put_text('Нам интересно, чему ты детей учишь?')
        elif User_data['gender']=='Мужской' and (post=='Ученик' or post=='Родитель'):
            put_text('\nДруг, ты вообще открывал учебник? :(\n').style('font-size: 20px; font-style: italic')
        elif User_data['gender']=='Женский' and (post=='Ученик' or post=='Родитель'):
            put_text('\nПодруга, ты вообще открывала учебник? :(\n').style('font-size: 20px; font-style: italic')
        put_text('Поработай над задачами номер : '+', '.join([str(i) for i in false_list])).style('font-size: 20px; font-style: italic')#Вывод не правильно решенных задач

    put_text("\nКол-во баллов: "+str(scores)+' из 100 возможных').style('color: green; font-size: 20px; font-style: italic')#Кол-во баллов
    put_text("\nРешено правильно: "+str(len(true_list))).style('color: green; font-size: 20px; font-style: italic') #Кол-во правильно решенных задач

    await AutoCerGen()

    if post=="Учитель" or post=="Родитель":
        msg=User_data['surname']+' '+User_data['name']+' '+User_data['patronymic'] +'\nЗавершил(-ла) работу и набрал(-ла) '+str(scores)+' баллов' #отправление письма с данными участника
    if post=="Ученик":
        msg=User_data['surname']+' '+User_data['name']+' '+User_data['patronymic']+'\n'+User_data['class']+User_data['letter']+'\nЗавершил работу и набрал(-ла) '+str(scores)+' баллов'#отправление письма с данными участника
    
    #await send_to_mail()

    cer_link=str('AutoCerGen/pictures/'+User_data['surname'] +' '+User_data['name']+' '+User_data['patronymic']+'.jpg')
    cer_file = open(cer_link, 'rb').read()    #Ссылка на загрузку сертификата
    put_file('certificate.jpg', cer_file, 'Скачать сертификат')

if __name__ == "__main__": #запуск сервера
    start_server(main, debug=False, port=8080, cdn=False, auto_open_webbrowser=True)