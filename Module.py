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
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


class School(db.Model):
    __tablename__ = 'School'
    school_id = db.Column('school_id', db.Integer, primary_key = True)
    name_en = db.Column(db.String, unique=True, nullable=False)
    name_kh = db.Column(db.String, unique=True, nullable=False)
    image = db.Column(db.ARRAY(db.String))
    pop_major_en = db.Column(db.ARRAY(db.String))
    pop_major_kh = db.Column(db.ARRAY(db.String))
    price_low = db.Column(db.Float)
    price_high = db.Column(db.Float)
    type_en = db.Column(db.String)
    type_kh = db.Column(db.String)
    bio_en = db.Column(db.String)
    bio_kh = db.Column(db.String)
    stand_point_en = db.Column(db.ARRAY(db.String))
    stand_point_kh = db.Column(db.ARRAY(db.String))
    mission_en = db.Column(db.String)
    mission_kh = db.Column(db.String)
    website = db.Column(db.ARRAY(db.String))
    tel = db.Column(db.ARRAY(db.String))
    email = db.Column(db.ARRAY(db.String))
    viewer = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    location = db.Column(db.Integer, db.ForeignKey('Location.location_id'))
    imgscenery = db.relationship('ImgScenery', backref = 'school_img')
    majors = db.relationship('School_Major', backref = 'school_majors')
    faculties = db.relationship('Faculty', backref = 'school_faculty')

    def __init__(self, name_en, name_kh, image, pop_major_en, pop_major_kh, price_low, price_high, type_en, type_kh, bio_en, bio_kh, stand_point_en, stand_point_kh, mission_en, mission_kh, website, tel, email, viewer, school_location):
        self.name_en = name_en
        self.name_kh = name_kh
        self.image = image
        self.pop_major_en = pop_major_en
        self.pop_major_kh = pop_major_kh
        self.price_low = price_low
        self.price_high = price_high
        self.type_en = type_en
        self.type_kh = type_kh
        self.bio_en = bio_en
        self.bio_kh = bio_kh
        self.stand_point_en = stand_point_en
        self.stand_point_kh = stand_point_kh
        self.mission_en = mission_en
        self.mission_kh = mission_kh
        self.website = website
        self.tel = tel
        self.email = email
        self.viewer = viewer
        self.school_location = school_location


class Location(db.Model):
    __tablename__ = 'Location'
    location_id = db.Column('location_id', db.Integer, primary_key = True)
    street_en = db.Column(db.String)
    street_kh = db.Column(db.String)
    district_en = db.Column(db.String)
    district_kh = db.Column(db.String)
    city_en = db.Column(db.String)
    city_kh = db.Column(db.String)
    province_en = db.Column(db.String)
    province_kh = db.Column(db.String)
    location_url = db.Column(db.String, nullable=False)
    school_id = db.relationship('School', backref = 'school_location', uselist = False)

    def __init__(self, street_en, street_kh, district_en, district_kh, city_en, city_kh, province_en, province_kh, location_url):
        self.street_en = street_en
        self.street_kh = street_kh
        self.district_en = district_en
        self.district_kh = district_kh
        self.city_en = city_en
        self.city_kh = city_kh
        self.province_en = province_en
        self.province_kh = province_kh
        self.location_url = location_url


class UserClient(db.Model):
    __tablename__ = 'UserClient'
    user_id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    total_post = db.Column(db.Integer)
    total_like = db.Column(db.Integer)
    user_profile = db.Column(db.String)
    imgscenery = db.relationship('ImgScenery', backref='img')
    baciipost = db.relationship('BacIIPost', backref='baciipost')
    baciicomment = db.relationship('BacIIComment', backref='baciicomment')

    def __init__(self, name, total_post, total_like, user_profile):
        self.name = name
        self.total_post = total_post
        self.total_like = total_like
        self.user_profile = user_profile


class ImgScenery(db.Model):
    __tablename__ = 'ImgScenery'
    img_id = db.Column('img_id', db.Integer, primary_key = True)
    img_url = db.Column(db.String)
    img_like = db.Column(db.Integer)
    school_id = db.Column(db.Integer, db.ForeignKey('School.school_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('UserClient.user_id'))

    # def __init__(self, img_url, img_like, school_id, user_id):
    #     self.img_url = img_url
    #     self.img_like = img_like
    #     self.school_img = school_id
    #     self.img = user_id


class Major(db.Model):
    __tablename__ = 'Major'
    id = db.Column('major_id',db.Integer, primary_key = True)
    name_en = db.Column(db.String, unique=True, nullable=False)
    name_kh = db.Column(db.String, unique=True, nullable=False)
    school_major = db.relationship('School_Major', backref = 'majors')

    # def __init__(self, name_en, name_kh):
    #     self.name_en = name_en
    #     self.name_kh = name_kh


class Faculty(db.Model):
    __tablename__ = 'Faculty'
    id = db.Column('faculty_id', db.Integer, primary_key = True)
    name_en = db.Column(db.String, nullable=False)
    name_kh = db.Column(db.String, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('School.school_id'))
    school_major = db.relationship('School_Major', backref = 'faculty_majors')

    def __init__(self, name_en, name_kh, school_id):
        self.name_en = name_en
        self.name_kh = name_kh
        self.school_faculty = school_id


class School_Major(db.Model):
    __tablename__ = 'School_Major'
    id = db.Column('sch_mar_id', db.Integer, primary_key = True)
    price = db.Column(db.Float)
    price_major = db.Column(db.ARRAY(db.Float))
    grade = db.Column(db.String(1))
    credit = db.Column(db.ARRAY(db.Integer))
    result = db.Column(db.String)
    faculty = db.Column(db.Integer, db.ForeignKey('Faculty.faculty_id'))
    major = db.Column(db.Integer, db.ForeignKey('Major.major_id'))
    school = db.Column(db.Integer, db.ForeignKey('School.school_id'))

    def __init__(self, price_major, grade, credit, result, faculty, major, school):
        self.price_major = price_major
        self.grade = grade
        self.credit = credit
        self.result = result
        self.faculty_majors = faculty
        self.majors = major
        self.school_majors = school


class SubjectBacII(db.Model):
  __tablename__ = "SubjectBacII"
  id = db.Column('sub_id', db.Integer, primary_key = True)
  name_en = db.Column(db.String, nullable=False, unique=True)
  name_kh = db.Column(db.String, nullable=False, unique=True)
  bacii_post = db.relationship('BacIIPost', backref = 'subject')


class BacIIPost(db.Model):
  __tablename__ = "BacIIPost"
  id = db.Column('post_id',db.Integer, primary_key = True)
  url = db.Column(db.ARRAY(db.String))
  time = db.Column(db.DateTime)
  react = db.Column(db.ARRAY(db.Integer))
  contents = db.Column(db.String)
  image = db.Column(db.ARRAY(db.String))
  userclient = db.Column(db.Integer, db.ForeignKey('UserClient.user_id'))
  subject_bacii = db.Column(db.Integer, db.ForeignKey('SubjectBacII.sub_id'))
  baciicomment = db.relationship('BacIIComment', backref = 'baciipost')


class BacIIComment(db.Model):
  __tablename__ = "BacIIComment"
  id = db.Column('com_id',db.Integer, primary_key = True)
  contents = db.Column(db.String)
  time = db.Column(db.DateTime)
  react = db.Column(db.ARRAY(db.Integer))
  userclient = db.Column(db.Integer, db.ForeignKey('UserClient.user_id'))
  bacii_post = db.Column(db.Integer, db.ForeignKey('BacIIPost.post_id'))
  bacii_reply = db.relationship('BacIIReplyComment', backref = 'comment')


class BacIIReplyComment(db.Model):
  __tablename__ = 'BacIIReplyComment'
  id = db.Column('rly_id',db.Integer, primary_key = True)
  userclient = db.Column(db.Integer, db.ForeignKey('UserClient.user_id'))
  contents = db.Column(db.String)
  baciicomment = db.Column(db.Integer, db.ForeignKey('BacIIComment.com_id'))
  time = db.Column(db.DateTime)
  react = db.Column(db.ARRAY(db.Integer))