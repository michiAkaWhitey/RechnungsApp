from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from database.dbHandler import DatabaseHandler

# connect to db
db = DatabaseHandler()
db.connectToDb(dbName='database/bills.db')

app = Flask(__name__)

# User verification
auth = HTTPBasicAuth()
users = {"admin": generate_password_hash("admin")}
@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    companies = db.companyNames()
    return render_template("bill.html", companies=companies) 

if __name__ == '__main__':
    app.run(debug=True)