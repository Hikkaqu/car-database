import sqlite3
from Car import Car
import os
import PrettyTable
import re

#Очищает консоль. Только на винде
clear = lambda: os.system('cls')  
clear()

db = sqlite3.connect("carDB.sqlite3")
cursor = db.cursor()

carList = []

#Автоматически создаёт новую таблицу, если данной не существует.
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cars' ''')
if cursor.fetchone()[0] != 1:
    cursor.execute(
        '''CREATE TABLE cars(id INTEGER PRIMARY KEY, brand TEXT, price INTEGER, year INTEGER, licensePlate TEXT, 
        isLeasingCar BOOLEAN)''')
    carList.append(Car("Mercedes", 9500000, 2018, "AB07354", 1))
    carList.append(Car("Citroën", 6000000, 2013, "B012345", 0))
    carList.append(Car("BMW", 5670000, 2020, "SC60856", 0))

    for c in carList:
        cursor.execute(''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                       (c.brand, c.price, c.year, c.licensePlate, c.isLeasingCar))
        db.commit()


def intro():
    clear()
    cursor.execute("SELECT COUNT (*) FROM cars")
    rowcount = cursor.fetchone()[0]   
    print("1. Показать все авто")
    print("2. Добавить авто")
    print("3. Убрать авто")
    print("4. Обновить авто")
    print("5. Показать определённое авто")
    print("6. Выход")
    userInput = input("Что вы выбрали? Введите номер\n")
    switch = 0
    while switch == 0:
        try:
            int(userInput)
        except ValueError:
            clear()
            print("Это не номер")
            input("Нажмите enter для продолжения")
            intro()
        else:
            switch = 1
    choice = int(userInput)
    if choice == 1:
        showAll()
    elif choice == 2:
        add()
    elif choice == 3:
        remove()
    elif choice == 4:
        update()
    elif choice == 5:
        showOne()
    elif choice == 6:
        clear()
        print("Сохранение авто и выход из программы")
    else:
        print("Это не опция")
        input("Нажмите enter для продолжения")
        intro()


def showAll():
    clear()
    cur = cursor.execute("SELECT * from cars")
    t = PrettyTable(["ID", "Brand", "Price [rub]", "Year", "License plate", "Is car leased?"])
    for row in cur:
        if row[5]:
            leasing = "Yes"
        else:
            leasing = "No"
        t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
    print(t)
    input("Нажмите enter для продолжения")
    intro()


def add():
    clear()
    print('Какой бренд у авто? Напишите "a" для отмены\n')
    brandInput = input('Или напишите "i" для импорта авто из bilhandel.dk\n')
    if brandInput.lower() == "a":
        intro()
    elif brandInput.lower() == "i":
        clear()
        url = input("Введите URL для авто, которое вы хотите импортировать\n")
        try:
            page = urlopen(url)
        except:
            print("Ошибка открытия URL")
        else:
            clear()
            soup = BeautifulSoup(page, 'html.parser')

            contentTitle = soup.find('div', {"class": "col-xs-8"})
            title = ''

            for x in contentTitle.findAll('h1'):
                title = title + ' ' + x.text
                if len(title) > 0:
                    titleSplit = title.split()
                    title = titleSplit[0]

                contentPrice = soup.find('div', {"class": "col-xs-4"})
                price = ''
                for x in contentPrice.findAll('div'):
                    price = price + ' ' + x.text

                contentYear = soup.find('div', {"style": "font-size: 16px;padding-left:15px;"})
                year = ''
                for x in contentYear.findAll('span'):
                    year = year + ' ' + x.text

                priceOutput = re.sub('\D', '', price)
                yearSplit = year.split()
                if len(yearSplit) > 0:
                    yearOutput = re.sub('\D', '', yearSplit[4])

                licensePlateInput = input("Какой номерной знак у авто?\n")
                isLeasingCarInput = input("Авто арендован?\n").lower()
                if isLeasingCarInput.startswith("j" or "y"):
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, licensePlateInput, 1))
                else:
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, licensePlateInput, 0))
                db.commit()
                intro()
    else:
        switch = 0
        while switch == 0:
            try:
                priceInput = float(input('Какая цена у авто?\n'))
            except ValueError:
                clear()
                print("This is not a number")
                input("Нажмите enter для продолжения")
            else:
                switch = 1
        switch = 0
        while switch == 0:
            try:
                yearInput = int(input("Какой год у авто?\n"))
            except ValueError:
                clear()
                print("Это не номер")
                input("Нажмите enter для продолжения")
            else:
                switch = 1
        licensePlateInput = input("Какой номерной знак у авто?\n")
        isLeasingCarInput = input("Авто арендован?\n").lower()
        if isLeasingCarInput.startswith("j" or "y"):
            cursor.execute(''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, licensePlateInput, 1))
        else:
            cursor.execute(''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, licensePlateInput, 0))
        db.commit()
        intro()


def remove():
    clear()
    cur = cursor.execute("SELECT id, brand, price, year, licensePlate, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [rub]", "Year", "License plate", "Is car leased?"])
    for row in cur:
        if row[5]:
            leasing = "Ja"
        else:
            leasing = "Nej"
        t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
        '''print(str(row[0]) + ".", row[1], "fra år ", row[2], "med nummepladen:", row[3])'''
    print(t)
    print('Какое авто вы хотите убрать? Введите ID')
    carID = input('Напишите "a" для отмены\n')
    if carID.lower() == "a":
        intro()
    else:
        switch = 0
        while switch == 0:
            try:
                float(carID)
            except ValueError:
                clear()
                print("Это не номер")
                input("Нажмите enter ля продолжения")
                remove()
            else:
                switch = 1
        sqlDelete = '''DELETE from cars where id=?'''
        sqlData = (int(carID))
        cursor.execute(sqlDelete, (int(sqlData),))
        db.commit()
        intro()


def update():
    clear()
    cur = cursor.execute("SELECT id, brand, price, year, licensePlate, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [rub]", "Year", "License plate", "Is car leased?"])
    for row in cur:
        if row[5]:
            leasing = "Yes"
        else:
            leasing = "No"
        t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
    print(t)
    print('Какую машину вы хотите обновить? Введите ID')
    carID = input('Напишите "a" для отмены\n')
    if carID.lower() == "a":
        intro()
    else:
        switch = 0
        while switch == 0:
            try:
                float(carID)
            except ValueError:
                clear()
                print("Это не номер")
                input("Нажмите enter ля продолжения")
                update()
            else:
                switch = 1
        switch1 = 0
        while switch1 == 0:
            sqlUpdate = ''' SELECT * from cars WHERE id =?'''
            sqlData = (int(carID))
            cur = cursor.execute(sqlUpdate, (int(sqlData),))
            clear()
            for row in cur:
                print("1. Бренд:", row[1])
                print("2. Цена:", row[2])
                print("3. Год:", row[3])
                print("4. Номерной знак:", row[4])
                if row[5] == 0:
                    print("5. Статус аренды: Авто не арендован")
                else:
                    print("5. Статус аренды: Авто арендован")
                print("6. Выход")
            userInput = input("Что вы хотите обновить? Введите номер\n")
            switch1 = 1
            switch2 = 0
            while switch2 == 0:
                try:
                    float(userInput)
                except ValueError:
                    clear()
                    print("Это не номер")
                    input("Нажмите enter для продолжения")
                else:
                    switch2 = 1
            if int(userInput) == 1:
                clear()
                sqlUpdate = ''' UPDATE cars SET brand =? WHERE id =? '''
                sqlData = input("Какой новый бренд у вашего авто?\n")
                cursor.execute(sqlUpdate, (sqlData, int(carID),))
                db.commit()
            if int(userInput) == 2:
                clear()
                sqlUpdate = ''' UPDATE cars SET price =? WHERE id =? '''
                switch3 = 0
                while switch3 == 0:
                    sqlData = input("Какая новая цена у вашего авто?\n")
                    try:
                        float(sqlData)
                    except ValueError:
                        clear()
                        print("Это не номер")
                        input("Нажмите enter для продолжения")
                    else:
                        switch3 = 1
                cursor.execute(sqlUpdate, (int(sqlData), int(carID),))
                db.commit()
            if int(userInput) == 3:
                clear()
                sqlUpdate = ''' UPDATE cars SET year =? WHERE id =? '''
                switch4 = 0
                while switch4 == 0:
                    sqlData = input("Какой год у вашего авто?\n")
                    try:
                        float(sqlData)
                    except ValueError:
                        clear()
                        print("Это не номер")
                        input("Нажмите enter для продолжения")
                    else:
                        switch4 = 1
                cursor.execute(sqlUpdate, (int(sqlData), int(carID),))
                db.commit()
            if int(userInput) == 4:
                clear()
                sqlUpdate = ''' UPDATE cars SET licensePlate =? WHERE id =? '''
                sqlData = input("Какой номерной знак для авто?\n")
                cursor.execute(sqlUpdate, (sqlData, int(carID),))
                db.commit()
            if int(userInput) == 5:
                clear()
                sqlUpdate = ''' UPDATE cars SET isLeasingCar =? WHERE id =? '''
                sqlData = input("Авто на аренде?\n").lower()
                if sqlData.startswith("j" or "y"):
                    sqlData = 1
                else:
                    sqlData = 0
                cursor.execute(sqlUpdate, (int(sqlData), int(carID),))
                db.commit()
            if int(userInput) == 6:
                clear()
                switch = 1
        update()


def showOne():
    clear()
    sqlSearch = ''' SELECT * from cars WHERE brand =?'''
    sqlData = (input("Поиск бренда: "))
    cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
    if cur.fetchone():
        clear()
        cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
        t = PrettyTable(["ID", "Brand", "Price [rub]", "Year", "License plate", "Is car leased?"])
        print("Показываю результаты для", sqlData)
        for row in cur:
            if row[5]:
                leasing = "Yes"
            else:
                leasing = "No"
            t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
        print(t)
        input("Нажмите enter для продолжения")
    else:
        clear()
        print("Нет результатов насчёт бренда", sqlData + ".")
        userInput = input("Хотите добавить новое авто?\n").lower()
        print(userInput)
        if userInput.startswith("j" or "y"):
            add()
        else:
            intro()
    intro()


intro()

db.commit()
db.close()
