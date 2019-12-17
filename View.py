from flask_security import current_user
from flask_admin import BaseView, expose
from flask_admin.contrib import sqla
from flask import request, abort
from Module import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
import random
import psycopg2
import datetime
import requests
import base64
import json

def uniqueID(len):
    letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    uniqueCode = ""
    for x in range(0,len):
        uniqueCode += letter[random.randrange(0,35)] 
    return uniqueCode

def getSubject(id):
    subject = db.session.query(SubjectBacII).filter_by(id = id).first()
    subject_en = None
    subject_kh = None
    if subject != None:
        subject_en = subject.name_en
        subject_kh = subject.name_kh
    return (subject_en, subject_kh)


def postImage(image_patch):
    API_ENDPOINT = "https://api.imgbb.com/1/upload"
    API_KEY = "4eea31e0d34fbec76e316d7cc9004ee9"
    # with open(image_patch, "rb") as imageFile:
    #     str_pic = base64.b64encode(imageFile.read())
    #     image = str_pic
    image = image_patch.read()
    data = {
        'key':API_KEY,
        'image':image
    }
    r = requests.post(url = API_ENDPOINT, data = data)
    pastebin_url = r.text
    pastebin_url = json.loads(pastebin_url)
    return pastebin_url



# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser'):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
    
    can_edit = True
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True


class UserAdminView(MyModelView):
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list


class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')


class UserView(MyModelView):
    column_editable_list = ['profileUrl','displayName']
    column_searchable_list = ["displayName"]
    column_filters = column_searchable_list


class SchoolView(BaseView):
    @expose('/', methods=['POST','GET'])
    def index(self):
        print("==================")
        if request.method == "POST":
            print(request.form.to_dict())
        _list = list()
        for i in range(1,100):
            _list.append({'row':i,'name_en':'English_en'+str(i),'name_kh':'Khmer'+str(i)})
        return self.render('admin/school_index.html', _list = _list)


class BacII_Post_View(BaseView):
    @expose('/', methods=['POST','GET'])
    def index(self):
        if request.method == "POST":
            data = request.form.to_dict()
            # return data
            if data['form_method'] == "save_subject_bacii":
                try:
                    subject_name_en = data['subject_name_en']
                    subject_name_kh = data['subject_name_kh']
                    id_code = uniqueID(6)
                    subject = SubjectBacII(id=id_code, name_en = subject_name_en, name_kh = subject_name_kh)
                    db.session.add(subject)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    self.index()
                except InvalidRequestError:
                    db.session.rollback()       
                    self.index()
                except psycopg2.errors.UniqueViolation:
                    db.session.rollback()
                    self.index()
            if data['form_method'] == "post_bacii":
                try:
                    owner = db.session.query(User).filter_by(id = "JDEDIXA3").first()
                    subject = db.session.query(SubjectBacII).filter_by(id = data["subject"]).first()
                    print(subject)
                    text_content = data["text_content"]
                    dateTime = datetime.datetime.now()
                    title = data["title"]
                    imageurl = data["imageurl"].split(",\r\n")
                    # image = postImage(data["imageurl"])
                    # image = postImage(request.files["imageurl"])
                    # return str(image)
                    # image = image.to_dict()
                    # if image.get("status") == 200:
                    #     imageurl = image.get("data").get("image").get("url")
                    #     imagethumb = image.get("data").get("thumb").get("url")
                    # return image
                    # [like, love, haha, wow, sad, angry]
                    react = [0,0,0,0,0]
                    id_code = uniqueID(10)
                    post = BacII_Post(id=id_code, datetime = dateTime, title = title, content = text_content, imageurl = imageurl,react = react,subject = subject,user = owner)
                    print(post)
                    db.session.add(post)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    self.index()
                except InvalidRequestError:
                    db.session.rollback()       
                    self.index()
                except psycopg2.errors.UniqueViolation:
                    db.session.rollback()
                    self.index()
            if data['form_method'] == "delete_subject":
                # try:
                subject = db.session.query(SubjectBacII).filter_by(id = data["subject_id"]).first()
                db.session.delete(subject)
                db.session.commit()
                # except Exception:
                #     print("Can't Delete")
        query_post = db.session.query(BacII_Post).order_by(BacII_Post.id.desc()).limit(5)
        post = []
        for x in query_post:
            subject = getSubject(x.subjectBacII)
            subject_en = subject[0]
            subject_kh = subject[1]
            post.append({'id':x.id, 'datetime':x.datetime,"react":x.react, 'title':x.title, 'content': x.content, 'imageurl':x.imageurl, "subject_en":subject_en, "subject_kh":subject_kh, 'owner':x.owner})
        list_subject = list()
        _object = SubjectBacII.query.all()
        for i in _object:
            list_subject.append({'row':i.id,'name_en':i.name_en,'name_kh':i.name_kh})
        return self.render('admin/bacii.html', post = post ,list_subject = list_subject)