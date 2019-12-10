#!venv/bin/python
import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_security.utils import encrypt_password
import flask_admin

from flask_admin import helpers as admin_helpers


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


# Define models
roles_users = db.Table(
    'roles_admin',
    db.Column('user_id', db.Integer(), db.ForeignKey('UserAdmin.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())

    def __str__(self):
        return self.name


class UserAdmin(db.Model, UserMixin):
    __tablename__ = "UserAdmin"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    confirmed_at = db.Column(db.DateTime())
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('admins', lazy='dynamic'))

    def __str__(self):
        return self.email


class School(db.Model):
    __tablename__ = 'School'
    id = db.Column('id', db.String(), primary_key = True)
    name_en = db.Column(db.String(), unique=True, nullable=False)
    name_kh = db.Column(db.String(), unique=True, nullable=False)
    media_url = db.Column(db.ARRAY(db.String()))
    pop_major_en = db.Column(db.ARRAY(db.String()))
    pop_major_kh = db.Column(db.ARRAY(db.String()))
    price_low = db.Column(db.Float())
    price_high = db.Column(db.Float())
    type_en = db.Column(db.String())
    type_kh = db.Column(db.String())
    bio_en = db.Column(db.String())
    bio_kh = db.Column(db.String())
    stand_point_en = db.Column(db.ARRAY(db.String()))
    stand_point_kh = db.Column(db.ARRAY(db.String()))
    mission_en = db.Column(db.String())
    mission_kh = db.Column(db.String())
    website = db.Column(db.ARRAY(db.String()))
    tel = db.Column(db.ARRAY(db.String()))
    email = db.Column(db.ARRAY(db.String()))
    viewer = db.Column(db.Integer())
    status = db.Column(db.Boolean())
    geo_location = db.Column(db.ARRAY(db.String))
    major_price = db.Column(db.Integer(), db.ForeignKey('Major_Price.id'))


class Major(db.Model):
    __tablename__ = 'Major'
    id = db.Column(db.Integer, primary_key = True)
    name_en = db.Column(db.String(), unique=True, nullable=False)
    name_kh = db.Column(db.String(), unique=True, nullable=False)
    price = db.relationship('Major_Price', backref = 'major', lazy='dynamic')


class Major_Price(db.Model):
    __tablename__ = 'Major_Price'
    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.ARRAY(db.Float()))
    method = db.Column(db.Integer())
    major_name = db.Column(db.Integer(), db.ForeignKey('Major.id'))
    school = db.relationship('School', backref='price', lazy = 'dynamic')


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.String(), primary_key = True)
    displayName = db.Column(db.String())
    profileUrl = db.Column(db.String())
    total_post = db.Column(db.Integer())
    total_like = db.Column(db.Integer())
    joindate = db.Column(db.DateTime())
    post = db.relationship("BacII_Post", backref="user", lazy="dynamic")
    comment = db.relationship("BacII_Comment", backref='bacii_comment', lazy="dynamic")
    comment_reply = db.relationship("Comment_Reply", backref='comment_reply', lazy="dynamic")
    image_Scenery = db.relationship("ImageScenary", backref="imageScenary", lazy="dynamic")


class SubjectBacII(db.Model):
    __tablename__ = "SubjectBacII"
    id = db.Column(db.String(), primary_key = True)
    name_en = db.Column(db.String(), nullable=False, unique=True)
    name_kh = db.Column(db.String(), nullable=False, unique=True)
    bacii_post = db.relationship('BacII_Post', backref="subject", lazy="dynamic")


class BacII_Post(db.Model):
    __tablename__ = "BacII_Post"
    id = db.Column(db.String(), primary_key = True)
    datetime = db.Column(db.DateTime())
    title = db.Column(db.String())
    content = db.Column(db.String())
    imageurl = db.Column(db.ARRAY(db.String()))
    react = db.Column(db.ARRAY(db.Integer()))
    subjectBacII = db.Column(db.String(), db.ForeignKey('SubjectBacII.id'))
    owner = db.Column(db.String(), db.ForeignKey("User.id"))
    comment = db.Column(db.String(), db.ForeignKey("BacII_Comment.id"))


class BacII_Comment(db.Model):
    __tablename__ = "BacII_Comment"
    id = db.Column(db.String(), primary_key = True)
    contents = db.Column(db.String())
    time = db.Column(db.DateTime())
    react = db.Column(db.ARRAY(db.Integer()))
    reply = db.Column(db.String(), db.ForeignKey("Comment_Reply.id"))
    owner = db.Column(db.String(), db.ForeignKey("User.id"))
    post = db.relationship("BacII_Post", backref="bacii_comment", lazy="dynamic")


class Comment_Reply(db.Model):
    __tablename__ = 'Comment_Reply'
    id = db.Column(db.String(), primary_key = True)
    contents = db.Column(db.String())
    time  = db.Column(db.DateTime())
    react = db.Column(db.ARRAY(db.Integer()))
    comment = db.relationship('BacII_Comment', backref="comment_reply", lazy='dynamic')
    owner = db.Column(db.String(), db.ForeignKey("User.id"))


class ImageScenary(db.Model):
    __tablename__ = 'ImageScenary'
    id = db.Column(db.String(), primary_key=True)
    imageUrl = db.Column(db.String())
    user_like = db.Column(db.ARRAY(db.String()))
    owner = db.Column(db.String(), db.ForeignKey("User.id"))
