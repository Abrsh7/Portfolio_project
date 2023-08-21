from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    return('hello bank')

@app.route('/login')
def login():
    return('login page')

@app.route('/register')
def register():
    return('register page')

@app.route('/deposite')
def deposite():
    return('deposite page')

@app.route('/withdraw')
def withdraw():
    return('withdraw page')

@app.route('/logout')
def logout():
    return('logout page')


if __name__ == "__main__":
  app.run(debug=True)
