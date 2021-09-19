from flask import Flask
from flask_restful import Resource
import pyodbc
import jsonpickle

driver = 'ODBC Driver 17 for SQL Server'
db_connection_string = f'DRIVER={driver};SERVER=tcp:eon-sb.database.windows.net,1433;' \
    f'DATABASE=esa;UID=app_login;PWD=4SB@pp_L0g1n;'\
    'Trusted_Connection=no;Connection Timeout=30;'

# Create connection to Azure SQL
conn = pyodbc.connect(db_connection_string)

def getGenericAccounts(self, account_id, email):     
    self.accountid = account_id
    self.email = email
    # account = {"AccountId": account_id}
    cursor = conn.cursor()    
    cursor.execute(f"Select * from dbo.Accounts where AccountID = ?", account_id)
    result = cursor.fetchone()  
    account_response = {'AccountId':result[0], 'Email':result[3]}

    cursor.close()
    return account_response, 200

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


