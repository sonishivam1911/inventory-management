import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


def fetch_database_connection():
    try:
        username = os.getenv('username')
        password = os.getenv('password')
        mydb = mysql.connector.connect(user=username, password=password, host='127.0.0.1', port=3306, database='inventorymanagement')
        return mydb
    except mysql.connector.Error as err:
        print(f"error : {err}")
    

def execute_query(query,return_record : bool = True):
    mydb = fetch_database_connection()
    cursor = mydb.cursor()
    cursor.execute(query)
    if return_record : 
        result = cursor.fetchall()
        cursor.close()
        mydb.close()
        return result
    else :
        mydb.close()
        cursor.close()



def execute_query_pandas(query):
    mydb = fetch_database_connection()
    output_df  = pd.read_sql(query,mydb)
    return output_df


def execute_procedures(procedure_name,arguments,return_record : bool = False):
    mydb = fetch_database_connection()
    cursor = mydb.cursor()
    result = cursor.callproc(procedure_name, arguments)
    if not return_record:
        mydb.commit()
        cursor.close()
        mydb.close()
    else:
        result = cursor.fetchall()
        cursor.close()
        mydb.close()
        return result

