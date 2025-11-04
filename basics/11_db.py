# Робота з базами даних
# 1. Встановлення СУБД. Використовуємо MySQL
# 2. Створюємо БД та користувача для неї (подаємо команди у Workbench)
# CREATE DATABASE server_221;
# CREATE USER user_knp_221@localhost IDENTIFIED BY 'pass_221';
# GRANT ALL PRIVILEGES ON server_221.* TO user_knp_221@localhost;
# 3. Додаємо драйвери підключення до БД
# pip install mysql-connector-python
import mysql.connector

db_ini = {
    'host': 'localhost',
    'port': 3308,  # 3306
    'user': 'user_knp_221',
    'password': 'pass_221',
    'database': 'server_221',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'use_unicode': True
}

db_connection = None

def connect_db() :
    global db_connection
    try :
        db_connection = mysql.connector.connect( **db_ini )
    except mysql.connector.Error as err :
        print(err)
    else :
        print("Connection OK")


def show_databases() :                        # Виконання SQL запитів
    global db_connection                      # 1. Контекст виконання команди (SqlCommand[ADO] Statement[JDBC])
    if db_connection is None : return         #     cursor [Python]
    try :                                     #    Контекст формує команду, передає її на виконання та
        cursor = db_connection.cursor()       #     контролює передачу результату (ітерування)
        cursor.execute("SHOW DATABASES")      #    Рекомендується для різних команд утворювати свої контексти,
    except mysql.connector.Error as err :     #     не виконуючи багатьох команд в одному контексті
        print(err)                            # 2. Виконання запиту (з результатами) запускає генератор
    else :                                    #     з боку СУБД, передача даних з якого відбувається
        print( cursor.column_names )          #     через ітерування курсора
        print('------------')                 # 3. Результат команди розділяється - окремо назви полів,
        for row in cursor :                   #     окремо самі результати
            print(row)                        # 4. Контекст команди має бути закритим для додаткового
    finally:                                  #     контролю того, що дані передані та ресурси звільнені
        cursor.close()                        # 


def show_uuid() :
    sql = "select uuid() as u1, uuid() as u2"
    global db_connection                      # 
    if db_connection is None : return
    try :                                     # Для спрощення доступу до результатів запитів
        cursor = db_connection.cursor(        # можна отримувати їх у формі словника (dict)
            dictionary=True                   # Це встановлюється додатковим параметром при
        )                                     # створенні курсора
        cursor.execute(sql)                   # 
    except mysql.connector.Error as err :     # 
        print(err)                            # 
        print(sql)                            # 
    else :                                    # 
        for row in cursor :                   # у результатах, що виводяться, імена колонок
            print(row)                        # включені до row
    finally:                                  # {'u1': '57e9e30b-b496-11f0-83b6-62517600596c', 'u2': '57e9e321-b496-11f0-83b6-62517600596c'}
        cursor.close()                        # 


def show_uuid2() :
    sql = "select uuid(), uuid()"
    global db_connection                      #
    if db_connection is None : return
    try :                                     #
        cursor = db_connection.cursor(        # Зворотній бік використання словника -
            dictionary=True                   # проблеми з колонками, що мають однакові імена
        )                                     # Для таких колонок
        cursor.execute(sql)                   # відбувається перезапис результатів
    except mysql.connector.Error as err :     # і замість кількох результатів
        print(err)                            # ми бачимо один
        print(sql)                            # {'uuid()': '57ea3bca-b496-11f0-83b6-62517600596c'}
    else :                                    # Така ситуація часто виникає, коли поєднуються декілька таблиць
        for row in cursor :                   #  у кожної з них є поле id, відповідно у поєднаному результаті
            print(row)                        #  буде декілька таких полів з однаковим іменем та !! різними
    finally:                                  #  значеннями
        cursor.close()                        # Однією з традицій БД є те, що у результатах запиту однакові імена
                                              # повинні мати однакові значення. Фактично це накладає умови на
                                              # іменування полів. Частіше за все - з префіксом таблиці

# Підготовлені (параметричні) запити - із розділенням запиту та його параметрів
# Вирішують проблему підстановки значень у запит при якій текст запиту може бути порушений
# INSERT ... VALUES(n)   n=1.5 через локалізацію число може бути подане як 1,5 що буде сприйматись як 2 параметри
def show_prep() :
    global db_connection                      # Prepared query
    if db_connection is None : return
    sql = "select datediff(" \
    "current_timestamp, %s)"                  # Режим "підготовленого запиту" зазначається
    try :                                     # при створенні курсора
        with db_connection.cursor(            # !! в старих версія драйвера за наявності prepared інші 
            prepared=True,                    #   параметри заборонялись
            dictionary=True                   # 
        ) as cursor :                         # Виконання передбачає передачу двох аргументів:
            cursor.execute(sql,               #  тексту запиту, що містить плейсхолдери
                       ('2025-10-01',))       #  набору параметрів для кожного плейсхолдера
            for row in cursor :               # 
                print(row)                    # 
    except mysql.connector.Error as err :     #
        print(err)                            # Використання блоку with дозволяє прибрати finally-close
        print(sql)                            # але змушує перегрупувати блок else
        
'''
Д.З. Реалізувати виконання запиту, який визначає різницю між поточною
датою та введеною користувачем, з включенням даних, що вводяться з
консолі програми. Перед передачею даних до запиту здійснити 
попередню валідацію на правильність дати, а також передбачити те,
що додаткову валідацію буде проведено СУБД
Введіть дату: 2025-10-01
Дата у минулому за 28 днів від поточної дати
Введіть дату: 2025-11-01
Дата у майбутньому через 3 дні від поточної дати
Введіть дату: 2025-10-29
Дата є поточною

'''        


def close_connection() :        
    db_connection.close()


def main() :                                  # 
    connect_db()                              # 
    show_databases()                          # 
    print('------------------------')
    show_uuid()
    print('------------------------')
    show_uuid2()
    print('------------------------')
    show_prep()
    close_connection()                        # 


if __name__ == '__main__' :
    main()
