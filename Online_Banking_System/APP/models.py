# Banking Website
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger

from APP import db, login_manager
from APP import bcrypt
from flask_login import UserMixin

from flask.globals import request


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(10), unique=True, nullable=False)
  email = db.Column(db.String(30), unique=True)
  password_hash = db.Column(db.String(length=60), nullable=False)
  
  accounts = db.relationship('Account', backref='user', lazy=True)
  transactions = db.relationship('Transaction', backref='user', lazy=True)
  

  def __repr__(self):
    return f'{self.username}, {self.email}, {self.password_hash}'
  @property
  def password(self):
    return self.password

  @password.setter
  def password(self, plain_text_password):
    self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password_hash, attempted_password)
  


class Account(db.Model):
  __tablename__ = 'accounts'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  account_no = db.Column(db.String(10), unique=True, nullable=False, index=True)
  balance = db.Column(db.Float, default=0.00)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

  transactions = db.relationship('Transaction', backref='account', lazy=True)

  def __repr__(self) -> str:
    return f'{self.account_no}'



class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accounts_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)

    def __repr__(self):
      return f'{self.user.username}'

db.create_all()











