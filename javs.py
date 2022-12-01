import mysql.connector
from mysql.connector import Error
import pandas as pd
import pickle
import sqlalchemy

#Upload data to database
def upload_data():
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS proyectoiot")
        cursor.execute("USE red")
        cursor.execute("CREATE TABLE IF NOT EXISTS entrada (id INT AUTO_INCREMENT PRIMARY KEY, temperatura INT, hora INT, luz INT, coffee INT, courtain INT)")
        luz=0
        coffee=0
        courtain=0
        temperature=0
        hour=0
        cursor.execute("INSERT INTO entrada (temperatura, hora, luz, coffee, courtain) VALUES (%s, %s, %s, %s, %s)", (temperatura, hora, luz, coffee, courtain))
        db.commit()
        print("Data uploaded")
    except Error as e:
        print("Error: ", e)
#Get data from database
def get_data():
    try:
        cursor.execute("USE red")
        cursor.execute("SELECT * FROM entrada")
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['id', 'temperatura', 'hora', 'luz', 'coffee', 'courtain'])
        return df
    except Error as e:
        print("Error: ", e)

def main():
    #Create the neural network
    print("Before")
    db = mysql.connector.connect(host = '3306', user = 'user', password = '', port = 3306,database='db')
    print("After")
    cursor = db.cursor()
    upload_data()
    df=get_data()
    print(df)
if "__main__" == __name__:
    main()