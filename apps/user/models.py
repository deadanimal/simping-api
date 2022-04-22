import requests
import json
import time
import os

from flask import Flask, render_template, flash, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required


from apps import db

class Base(db.Model):

    __abstract__  = True

    id = db.Column(db.BigInteger, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class RolesUsers(Base):
    __tablename__ = 'roles_users'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column('user_id', db.BigInteger(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.BigInteger(), db.ForeignKey('role.id'))


class Role(Base, RoleMixin):
    
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(Base, UserMixin):

    __tablename__ = 'user'

    username = db.Column(db.String(256), unique=True, nullable=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    phone_country_code = db.Column(db.Integer(), nullable=True)
    phone_number = db.Column(db.Integer(), nullable=True)

    wallet_public = db.Column(db.String(255))
    wallet_secret = db.Column(db.String(255))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
