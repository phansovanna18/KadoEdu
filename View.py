from flask_security import current_user
from flask_admin import BaseView, expose
from flask_admin.contrib import sqla
from flask import request

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


    # can_edit = True
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


class LocationView(MyModelView):
  column_editable_list = ['street_en', 'street_kh', 'district_en', 'district_kh']
  column_searchable_list = column_editable_list
  column_exclude_list = ['imgscenery', 'baciipost', 'baciicomment']
  form_excluded_columns = column_exclude_list
  column_details_exclude_list = column_exclude_list
  column_filters = column_editable_list


class UserClientView(MyModelView):
  column_editable_list = ['name', 'total_post', 'total_like', 'user_profile']
  column_searchable_list = column_editable_list
  column_exclude_list = ['imgscenery', 'baciipost', 'baciicomment']
  form_excluded_columns = column_exclude_list
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
        from Module import UserClient
        school = UserClient.query.all()
        # for x in school:
        #     _list.append({'totol_post':x.total_post})
        for i in range(1,100):
            _list.append({'row':i,'name_en':'English_en'+str(i),'name_kh':'Khmer'+str(i)})
        # new_list = sorted(_list, key=lambda k: k['name_en'])
        return self.render('admin/school_index.html', _list = _list)
    # @expose('/add/', methods=['POST','GET'])
    # def add(self):
    #     from flask import redirect,url_for
    #     # print(request.form.to_dict())
    #     return redirect(url_for('school.index'))



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



class BacIIContentView(BaseView):
    @expose('/')
    def index(self):
        _list = list()
        from Module import UserClient
        for i in range(1,10):
            _list.append({'row':i,'name_en':'English'+str(i),'name_kh':'Khmer'+str(i)})
        return self.render('admin/bacii.html', _list = _list)