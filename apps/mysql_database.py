import mysql.connector
from mysql.connector import errorcode

# declaring global variables
DB_NAME="final_year_project"
resultlist1=[]


# code for database building
def build_database():
    try:
        cnx = mysql.connector.connect(
          host="localhost",
          user="root",
          password="Ashutosh@123456"
        )
        cursor=cnx.cursor()
        print('connection established successfully')
    except:
        print('Connection establishment failed')
    #finally:
        #cursor.close()
        #cnx.close()
    global DB_NAME
    #DB_NAME="pblproject6"

    TABLES = {}

    TABLES['customers'] = ("CREATE TABLE `customers` ("
        "  `customer_no` int(11) NOT NULL AUTO_INCREMENT,"
        "  `first_name` char(20) NOT NULL,"
        "  `last_name` char(20) NOT NULL,"
        "  `username` varchar(20) NOT NULL,"
        "  `password` varchar(20) NOT NULL,"
        "  `email` varchar(20) NOT NULL,"
        "  PRIMARY KEY (`customer_no`)"
        ") ENGINE=InnoDB")


    TABLES['stocks'] = ("CREATE TABLE `stocks` ("
        "  `trade_no` int(11) NOT NULL AUTO_INCREMENT,"
        "  `stock_name` char(20) NOT NULL,"
        "  `quantity` int(11) NOT NULL,"
        "  `price` int(11) NOT NULL,"
        "  `time_of_buying` timestamp NOT NULL,"
        "  `time_of_selling` timestamp ,"
        "  `associated_customer_username` varchar(20) NOT NULL,"
        "  `status` char(20) NOT NULL,"
        "  PRIMARY KEY (`trade_no`)"
        ") ENGINE=InnoDB")

    def create_database(cursor):
        try:
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            #exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            #exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()


def register_customer(firstname,lastname,email,username,password):
    try:
        mydb = mysql.connector.connect(host="localhost",user="root",password="Ashutosh@123456",database="final_year_project")
        mycursor = mydb.cursor()
        sql = "INSERT INTO customers (firstname,lastname,username,password,email) VALUES (%s, %s,%s, %s, %s)"
        val = (firstname,lastname,username,password,email)
        mycursor.execute(sql, val)
        mydb.commit()
        return 1
    except mysql.connector.Error as err:
        print("Customer cannot be registerd")
        return 0
