from flask import Flask
from datetime import datetime
from flask import render_template
from flask_restful import reqparse, Api, Resource
from dbConnection import *

app = Flask("My Test Flask")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template("hello_there.html", name=name, date=datetime.now())


@app.route("/accounts/<accountid>")
def getAccount(accountid):     
    # account = {"AccountId": account_id}
    cursor = conn.cursor()    
    cursor.execute(f"Select * from dbo.Accounts where AccountID = ?", accountid)
    result = cursor.fetchone()  
    cursor.close()

    if result is not None and len(result) > 0:
        return render_template("accounts.html", accountId=result[0], email=result[3])
    else:
        return render_template("accounts.html")


@app.route("/accounts")
def getAccounts():     
    # account = {"AccountId": account_id}
    cursor = conn.cursor()    
    cursor.execute(f"Select top 10 * from dbo.Accounts order by AccountID desc")
    results = cursor.fetchall()    
    account_response = {}
    index = 0
    for account in results:
        account_response[index] = {'AccountId':account[0], 'Email':account[3]}
        index = index + 1
    cursor.close()

    if results is not None and len(results) > 0:
        return render_template("accounts.html", accounts=account_response)
    else:
        return render_template("accounts.html")


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/api/genericAccounts")
def get_generic_accounts():
    return getGenericAccounts()

# Setup Flask Restful framework
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('Accounts')

# Create API route to defined Customer class
api.add_resource(Accounts, '/api/accounts')
api.add_resource(Account, '/api/account', '/api/account/<account_id>')
