# DAO/DAL - Data Access Object / Layer - архітектурний шар, що 
# інкапсулює роботу з даними, надаючи програмний інтерфейс
import hashlib 
import json
import mysql.connector
import sys

class DataAccessor :
    def __init__(self, ini_file="./db.json"):
        try :
            with open(ini_file, encoding="utf-8") as file :
                self.ini = json.load(file)
        except OSError as err :
            raise RuntimeError("Ini read error: " + str(err))
        
        try :
            self.db_connection = mysql.connector.connect( **self.ini )
        except mysql.connector.Error as err :
            raise RuntimeError("Connection error: " + str(err))


    def install(self) :
        try :
            self._install_users()
            self._install_roles()
            self._install_user_access()
            self._install_tokens()
        except Exception as err :
            print(err)


    def _install_users(self) :
        sql = '''CREATE TABLE  IF NOT EXISTS  users (
            user_id             CHAR(36)     NOT NULL PRIMARY KEY DEFAULT( UUID() ),
            user_name           VARCHAR(64)  NOT NULL,
            user_email          VARCHAR(128) NOT NULL,
            user_birthdate      DATETIME         NULL,
            user_registered_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
            user_deleted_at     DATETIME         NULL
        ) ENGINE = InnoDb   DEFAULT CHARSET = utf8mb4   COLLATE = utf8mb4_unicode_ci
        '''
        if self.db_connection is None : 
            raise RuntimeError("Connection empty in _install_users")
        with self.db_connection.cursor() as cursor :
            cursor.execute(sql)


    def _install_roles(self) :
        sql = '''CREATE TABLE  IF NOT EXISTS  roles (
            role_id             VARCHAR(16)  NOT NULL PRIMARY KEY,
            role_description    VARCHAR(512) NOT NULL,
            role_can_create     TINYINT      NOT NULL DEFAULT 0,
            role_can_read       TINYINT      NOT NULL DEFAULT 0,
            role_can_update     TINYINT      NOT NULL DEFAULT 0,
            role_can_delete     TINYINT      NOT NULL DEFAULT 0
        ) ENGINE = InnoDb   DEFAULT CHARSET = utf8mb4   COLLATE = utf8mb4_unicode_ci
        '''
        if self.db_connection is None : 
            raise RuntimeError("Connection empty in _install_roles")
        with self.db_connection.cursor() as cursor :
            cursor.execute(sql)


    def _install_user_access(self) :
        sql = '''CREATE TABLE  IF NOT EXISTS  user_accesses (
            user_access_id      CHAR(36)     NOT NULL PRIMARY KEY DEFAULT( UUID() ),
            user_id             CHAR(36)     NOT NULL,
            role_id             VARCHAR(16)  NOT NULL,
            user_access_login   VARCHAR(32)  NOT NULL,
            user_access_salt    CHAR(16)     NOT NULL,
            user_access_dk      CHAR(20)     NOT NULL COMMENT 'Derived Key by RFC 2898',
            UNIQUE(user_access_login)
        ) ENGINE = InnoDb   DEFAULT CHARSET = utf8mb4   COLLATE = utf8mb4_unicode_ci
        '''
        if self.db_connection is None : 
            raise RuntimeError("Connection empty in " + sys._getframe(0).f_code.co_name)
        with self.db_connection.cursor() as cursor :
            cursor.execute(sql)
    

    def _install_tokens(self) :
        sql = '''CREATE TABLE  IF NOT EXISTS  tokens (
            token_id         CHAR(36)     NOT NULL PRIMARY KEY DEFAULT( UUID() ),
            user_access_id   CHAR(36)     NOT NULL,
            token_issued_at  DATETIME     NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            token_expired_at DATETIME     NOT NULL,
            token_type       VARCHAR(16)      NULL
        ) ENGINE = InnoDb   DEFAULT CHARSET = utf8mb4   COLLATE = utf8mb4_unicode_ci
        '''
        if self.db_connection is None : 
            raise RuntimeError("Connection empty in " + sys._getframe(0).f_code.co_name)
        with self.db_connection.cursor() as cursor :
            cursor.execute(sql)
            

    def _hash(self, input:str) -> str :
        hash = hashlib.sha3_256()  
        hash.update(input.encode(encoding='utf-8'))
        return hash.hexdigest()


    def kdf1(self, password:str, salt:str) -> str :
        iteration_count = 1000    # RFC 2898 recommendation
        dk_len = 20
        t = self._hash(password + salt)
        for i in range(iteration_count) :
            t = self._hash(t)
        return t[:dk_len]    


    def _seed_users() :
        '''Сідування (seed - зерно) - утворення початкових значень в алгоритмі чи БД
        Для БД користувачів необхідно щонайменше 2 ролі - максимальна (admin) та мінімальна (guest)
        а також користувач (user + access) з максимальною роллю'''



def main() :
    try :
        data_accessor = DataAccessor()
    except RuntimeError as err :
        print(err)
        return
    else :
        # data_accessor.install()
        print(data_accessor.kdf1("123", "456"))  # 72c94aeca814edb0e7c1
        print("Commands OK")



if __name__ == '__main__' :
    main()

'''
Д.З. Створити імплементацію функції PBKDF2
https://datatracker.ietf.org/doc/html/rfc2898#section-5.2
Провести випробування, додати скріншоти роботи
'''