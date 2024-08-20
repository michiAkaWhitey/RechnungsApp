from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# User verification
auth = HTTPBasicAuth()
users = {"admin": generate_password_hash("admin")}
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/', methods = ['POST', 'GET'])
@auth.login_required
def index():
    return render_template("index.html")

@app.post("/foo")
def foo_post():
    print('x')
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)