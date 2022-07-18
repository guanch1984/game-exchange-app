from getpass import getpass
# from ssl import _PasswordType
from mysql.connector import connect, Error, MySQLConnection
import random




def testRegisterNewUser(username, user_nickname ):
    """ Connect to MySQL database """

    db_config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'port': 8000, 'database':'cs6400_summer2022_team065'}
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')
        cursor = conn.cursor()

        user_postalcode = "71455"
        query = "INSERT INTO TradePlazaUser (email, password, nickname, first_name, last_name, postal_code) VALUES " + \
                "(\"" + username + "\", \"" + username + "\", \"" + user_nickname + "\", \"" + user_nickname + "\", \"" + \
                    username + "\", \"" + user_postalcode + "\")"
        print(query)
        cursor.execute(query)
        conn.commit()
    except Error as error:
        print("error registering user")
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')
            
def loginRegisteredUserWithEmail(username, user_nickname):
    """ Connect to MySQL database """

    db_config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'port': 8000, 'database':'cs6400_summer2022_team065'}
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')
        cursor = conn.cursor()
        query = "SELECT email from TradePlazaUser where (TradePlazaUser.email=" + "\"" + username  + \
            "\"" + ") and TradePlazaUser.password=" + "\"" + username  + "\""
        print(query)
        cursor.execute(query)
        res = cursor.fetchall()
        print(res)
        if len(res) == 1:
            print("user found and logged in")
        else:
            print("user not found, unable to login")
    except Error as error:
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')


def loginRegisteredUserWithNickName(username, user_nickname):
    """ Connect to MySQL database """

    db_config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'port': 8000, 'database':'cs6400_summer2022_team065'}
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')
        cursor = conn.cursor()
        query = "SELECT email from TradePlazaUser where (TradePlazaUser.nickname=" + "\"" + user_nickname  + \
            "\"" + ") and TradePlazaUser.password=" + "\"" + username  + "\""
        print(query)
        cursor.execute(query)
        res = cursor.fetchall()
        print(res)
        if len(res) == 1:
            print("user found and logged in")
        else:
            print("user not found, unable to login")
    except Error as error:
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')

if __name__ == '__main__':
    db_config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'port': 8000, 'database':'cs6400_summer2022_team065'}
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')
    except Error as error:
        print(error)
        
    username = "user " + str(round(random.random(), 3))
    user_nickname = "user " + str(round(random.random(), 3))
    testRegisterNewUser(username, user_nickname)
    loginRegisteredUserWithEmail(username, user_nickname)
    loginRegisteredUserWithNickName(username, user_nickname)