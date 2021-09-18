from flask import Flask
from flask_restful import Resource
import pyodbc

driver = 'ODBC Driver 17 for SQL Server'
db_connection_string = f'DRIVER={driver};SERVER=tcp:eon-sb.database.windows.net,1433;' \
    f'DATABASE=esa;UID=app_login;PWD=4SB@pp_L0g1n;'\
    'Trusted_Connection=no;Connection Timeout=30;'

# Create connection to Azure SQL
conn = pyodbc.connect(db_connection_string)

# Customer Class
class Account(Resource):
    def get(self, account_id):     
        # account = {"AccountId": account_id}
        cursor = conn.cursor()    
        cursor.execute(f"Select * from dbo.Accounts where AccountID = ?", account_id)
        result = cursor.fetchone()  
        account_response = {'AccountId':result[0], 'Email':result[3]}

        cursor.close()
        return account_response, 200
    
class Accounts(Resource):
    def get(self):     
        cursor = conn.cursor()    
        cursor.execute(f"Select top 10 * from dbo.Accounts order by AccountID desc")
        results = cursor.fetchall()
        cursor.close()
        account_response = {}
        index = 0
        for account in results:
            account_response[index] = {'AccountId':account[0], 'Email':account[3]}
            index = index + 1

        return account_response, 200


