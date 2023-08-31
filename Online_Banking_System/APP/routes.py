from APP import app
from flask import render_template, request, session, url_for, redirect, flash
from APP.models import User, Account, Transaction
from APP.forms import RegistrationForm, LoginForm
from APP import db
from flask_login import login_user
import random
import string

@app.route('/')
def homepage():
   return render_template('homepage.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    attempted_user = User.query.filter_by(username=form.username.data).first()
    if attempted_user and attempted_user.check_password_correction(
       attempted_password=form.password.data
        ):
        login_user(attempted_user)
        flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
        return redirect(url_for('account'))
    else:
      flash('Username and password are not match! Please try again', category='danger')
  return render_template('login.html', form=form)


@app.route('/register', methods= ['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('homepage'))
  if form.errors != {}: #If there are not errors from the validations
     for err_msg in form.errors.values():
       flash(f'There was an error with creating a user: {err_msg}', category='danger')
  return render_template('register.html', form=form)

def generate_account_number():
    # Generate a random alphanumeric account number of length 10
    alphanumeric = string.ascii_uppercase + string.ascii_lowercase + string.digits
    account_number = ''.join(random.choices(alphanumeric, k=10))
    return account_number

@app.route('/account', methods= ['GET', 'POST'])
def account():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    user = User.query.get(user_id)

    return render_template('account.html', user=user)

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    user = User.query.get(user_id)

    account_id = request.form['account_id']
    amount = float(request.form['amount'])

    account = Account.query.get(account_id)

    # Update the account balance
    account.balance += amount

    # Create a deposit transaction
    transaction = Transaction(account_id=account_id, amount=amount, transaction_type='deposit')
    db.session.add(transaction)
    db.session.commit()

    return redirect('/account')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    user = User.query.get(user_id)

    account_id = request.form['account_id']
    amount = float(request.form['amount'])

    account = Account.query.get(account_id)

    # Check if the withdrawal amount is valid
    if account.balance >= amount:
        # Update the account balance
        account.balance -= amount

        # Create a withdrawal transaction
        transaction = Transaction(account_id=account_id, amount=amount, transaction_type='withdrawal')
        db.session.add(transaction)
        db.session.commit()
    else:
        return 'Insufficient balance'

    return redirect('/account')

@app.route('/transfer', methods=['POST'])
def transfer():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    user = User.query.get(user_id)

    from_account_id = request.form['from_account_id']
    to_account_id = request.form['to_account_id']
    amount = float(request.form['amount'])

    from_account = Account.query.get(from_account_id)
    to_account = Account.query.get(to_account_id)

    # Check if the transfer amount is valid
    if from_account.balance >= amount:
        # Update the account balances
        from_account.balance -= amount
        to_account.balance += amount

        # Create a withdrawal transaction
        withdrawal_transaction = Transaction(account_id=from_account_id, amount=amount, transaction_type='withdrawal')
        db.session.add(withdrawal_transaction)

        # Create a deposit transaction
        deposit_transaction = Transaction(account_id=to_account_id, amount=amount, transaction_type='deposit')
        db.session.add(deposit_transaction)

        db.session.commit()
    else:
        return 'Insufficient balance'

    return redirect('/account')

@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('homepage'))