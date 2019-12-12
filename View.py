from flask_security import current_user
from flask_admin import BaseView, expose
from flask_admin.contrib import sqla
from flask import request, abort
from Module import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
import random
import psycopg2

def uniqueID(len):
    letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    uniqueCode = ""
    for x in range(0,len):
        uniqueCode += letter[random.randrange(0,35)] 
    return uniqueCode


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


class UserView(MyModelView):
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



class SchoolPriceView(BaseView):
    @expose('/')
    def index(self):
        _list = list()
        from Module import UserClient
        school = UserClient.query.all()
        # for x in school:
        #     _list.append({'totol_post':x.total_post})
        for i in range(1,10):
            _list.append({'row':i,'name_en':'English'+str(i),'name_kh':'Khmer'+str(i)})
        # new_list = sorted(_list, key=lambda k: k['name_en'])
        return self.render('admin/school_price.html', _list = _list)



class BacII_Post_View(BaseView):
    @expose('/', methods=['POST','GET'])
    def index(self):
        if request.method == "POST":
            data = request.form.to_dict()
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
        list_subject = list()
        subject = list()
        _object = SubjectBacII.query.all()
        print(_object)
        for i in _object:
            list_subject.append({'row':i.id,'name_en':i.name_en,'name_kh':i.name_kh})
        for i in range(1,110):
            subject.append(i)
        return self.render('admin/bacii.html', _list = list_subject, subject = subject)