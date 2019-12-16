from Module import *


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, UserAdmin, Role)
security = Security(app, user_datastore)

# Flask views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/getpost')
def getpost():
    query = db.session.query(BacII_Post).order_by(BacII_Post.id.desc()).limit(5)
    query = query[::-1]
    _list = list()
    if query != None:
        for x in query:
            subject = db.session.query(SubjectBacII).filter_by(id = x.subjectBacII).first()
            subject_en = None
            subject_kh = None
            if subject != None:
                subject_en = subject.name_en
                subject_kh = subject.name_kh
            owner = db.session.query(User).filter_by(id = x.owner).first()
            _list.append({'id':x.id, 'datetime':x.datetime, 'title':x.title, 'content': x.content, 'imageurl':x.imageurl, "subject_en":subject_en, "subject_kh":subject_kh, 'owner':x.owner})
        return jsonify({"result":_list, "state":1})
    return jsonify({"state":0})


# Create admin
admin = flask_admin.Admin(
    app,
    'Kado Edu',
    base_template='my_master.html',
    template_mode='bootstrap3',
)


from View import *

# Add model views

admin.add_view(SchoolView(name="School", endpoint='school', menu_icon_type='fa', menu_icon_value='fa-connectdevelop'))
# admin.add_view(SchoolPriceView(name="School Price", endpoint='schoolprice', menu_icon_type='fa', menu_icon_value='fa-connectdevelop',))
# admin.add_view(BacIIContentView(name="Bac II Content", endpoint='bacii', menu_icon_type='fa', menu_icon_value='fa-connectdevelop',))
admin.add_view(CustomView(name="Custom view", endpoint='custom', menu_icon_type='fa', menu_icon_value='fa-connectdevelop',))
# admin.add_view(UserClientView(UserClient, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="User Client"))
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Roles"))
admin.add_view(UserAdminView(UserAdmin, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="UserAdmin"))
admin.add_view(BacII_Post_View(name="BacII", endpoint="bacii", menu_icon_type='fa', menu_icon_value='fa-users'))
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

#data sample
def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='AdminKado',
            email='admin',
            password=encrypt_password('adminkado'),
            roles=[user_role, super_user_role]
        )

        user = User(id = "JDEDIXA3", displayName = "Admin",profileUrl = "https://avatars1.githubusercontent.com/u/45761736?s=400&u=0d5c4f046fdc2bc8682cb99d9d4d611eda87010c&v=4", total_post = 0, total_like = 0, joindate = datetime.datetime.now())
        db.session.add(user)
        db.session.commit()
    return


if __name__ == '__main__':
    # build_sample_db()
    # Start app
    app.run(debug=True)
