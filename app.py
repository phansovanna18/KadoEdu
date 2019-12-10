from Module import *


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, UserAdmin, Role)
security = Security(app, user_datastore)

# Flask views
@app.route('/')
def index():
    return render_template('index.html')




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
admin.add_view(UserView(UserAdmin, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(BacII_Post_View(name="BacII", endpoint="bacii", menu_icon_type='fa', menu_icon_value='fa-users'))

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
        db.session.commit()
    return

if __name__ == '__main__':
    # build_sample_db()
    # Start app
    app.run(debug=True)