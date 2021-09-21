from flask import Flask
from flask_restful import Resource
import pyodbc
import jsonpickle
import csv

driver = 'ODBC Driver 17 for SQL Server'
db_connection_string = f'DRIVER={driver};SERVER=tcp:eon-sb.database.windows.net,1433;' \
    f'DATABASE=esa;UID=app_login;PWD=4SB@pp_L0g1n;'\
    'Trusted_Connection=no;Connection Timeout=30;'

# Create connection to Azure SQL
conn = pyodbc.connect(db_connection_string)

# Customer Class    
class Account(Resource):
    def get(self, account_id):     
        cursor = conn.cursor()    
        cursor.execute(f"Select * from dbo.Accounts where AccountID = ?", account_id)
        result = cursor.fetchone()  
        self.accountid = result[0]
        self.email = result[3]

        cursor.close()
        return jsonpickle.encode(self)

class Accounts(Resource):
    def __init__(self):
        self.accounts = []
    def get(self):     
        cursor = conn.cursor()    
        cursor.execute(f"Select top 10 * from dbo.Accounts order by AccountID desc")
        results = cursor.fetchall()
        cursor.close()
        for account in results:
            self.accounts.append({'AccountId':account[0], 'Email':account[3]})
        return jsonpickle.encode(self)

class Hotels(Resource):
    def get(self):
        with open('eng_playbook_hotels.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            index = 0
            for row in spamreader:
                if (index == 0):
                    index = index + 1
                else:                   

                    cursor = conn.cursor()    
                    cursor.execute(f"insert into hotels values (?, ?, ?)"
                    # cursor.execute(f"if not exists (select 1 from hotels where id = ?) " \
                    #                 "begin " \
                    #                     "insert into hotels values (?, ?, ?) " \
                    #                 "end "
                                        , row[0], row[1], row[2])
                    cursor.commit()
                    cursor.close()
                    index = index + 1