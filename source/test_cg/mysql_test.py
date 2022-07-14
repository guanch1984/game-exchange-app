from getpass import getpass
# from ssl import _PasswordType
from mysql.connector import connect, Error, MySQLConnection

# try:
#     with connect(
#         host="localhost",
#         user='root',
#         password = 'eAqXuV=U-Yg2xM5e',
#         # user=input("Enter username: "),
#         # password=getpass("Enter password: "),
#     ) as connection:
#         print('successssss')
#         print(connection)
# except Error as e:
#     print('failllll')
#     print(e)

def connect():
    """ Connect to MySQL database """

    db_config = {'host': 'localhost', 'user': 'root', 'password': 'eAqXuV=U-Yg2xM5e'}
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

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')


if __name__ == '__main__':
    connect()