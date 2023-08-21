from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/deposite')
def deposite():
    return render_template('deposit.html')

@app.route('/withdraw')
def withdraw():
    return render_template('withdraw.html')

@app.route('/logout')
def logout():
    return redirect(url_for('homepage'))


if __name__ == "__main__":
  app.run(debug=True)
