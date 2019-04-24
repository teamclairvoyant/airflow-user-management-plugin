__author__ = 'robertsanders'

import airflow
from airflow import configuration
from airflow.plugins_manager import AirflowPlugin
from airflow.contrib.auth.backends.password_auth import PasswordUser
from airflow.settings import Session
from airflow.models import User

from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView

from flask import Markup
from flask import Blueprint, flash

from wtforms import PasswordField, BooleanField
from flask_login import current_user

from sqlalchemy import func

import logging

def email_formatter(v, c, m, p):
    return Markup('<a href="mailto:{m.email}">{m.email}</a>'.format(**locals()))

"""
Utility function to check if the logged in User is a super user or not.
Note: Airflow User Model object has a superuser attribute, but its not persisted in the database until versions >= 2.0
"""
def is_super_user(self):
    airflow_version = airflow.__version__
    if float(airflow_version[:3]) <= 1.10:
        """
        We need to add the following configuration in the airflow.cfg file for versions < 2.0
        [user_management_plugin]
        #provide comma separated list of admin users
        #Ex: admin_users=admin,airflow
        admin_users=airflow
        """
        users = configuration.get("user_management_plugin", "admin_users") if configuration.has_option("user_management_plugin", "admin_users" ) else ""
        if users != "":
            admin_users = users.split(",")
            if admin_users.__contains__(current_user.user.username):
                return True
        else:
            logging.error("No Admin users were provided")
            return False
    else:
        # For versions >= 2.0 we check for the superuser flag
        return current_user.user.superuser


class UserManagementModelView(ModelView):
    # http://flask-admin.readthedocs.io/en/latest/api/mod_model/

    verbose_name_plural = "User Management - Password Users"
    verbose_name = "User Management - Password User"
    list_template = 'airflow/model_list.html'
    edit_template = 'airflow/model_edit.html'
    create_template = 'airflow/model_create.html'

    column_display_actions = True
    # page_size = 500
    can_set_page_size = True

    can_create = True
    can_edit = True
    can_delete = True

    column_list = ('id', 'username', 'email')
    column_formatters = dict(email=email_formatter)
    column_searchable_list = ('username', 'email')

    form_columns = ('username', 'email', 'password', 'password_confirm', 'superuser')
    form_extra_fields = {
        'password_confirm': PasswordField('Password (Confirm)'),
        'superuser': BooleanField( 'superuser' )
    }
    form_widget_args = {
        'password': {
            'type': "password"
        }
    }
    # form_create_rules = None
    # form_args = dict(
    #     email=dict(validators=[])
    # )

    def on_form_prefill(self, form, id):
        if (not is_super_user(self)):
            form.username.render_kw = {'readonly': True}
            form.superuser.render_kw = {'readonly': True}

    def on_model_change(self, form, model, is_created):
        logging.info("UserManagementModelView.on_model_change(form=" + str(form) + ", model=" + str(model) + ", is_created=" + str(is_created) + ")")
        logging.info("Confirm Password:" + form.password_confirm.data )
        return super(UserManagementModelView, self).on_model_change(form, model, is_created)

    # Added the override for get_query so that the admin can see all the users while other's can see only their record displayed.
    def get_query(self):
        if is_super_user(self):
            return self.session.query( self.model )

        return self.session.query( self.model ).filter( self.model.username == current_user.user.username )

    # Added the override for get_count_query so that the admin can see the count of all users while other's can see only one row displayed.
    def get_count_query(self):
        if is_super_user(self):
            return self.session.query(func.count('*')).filter(self.model.username != '')

        return self.session.query(func.count('*')).filter(self.model.username == current_user.user.username)

    # Overrides the create_model function to create the User object required to create the PasswordUser object
    def create_model(self, form):
        if is_super_user(self):
            logging.info("UserManagementModelView.create_model(form=" + str(form) + ")")
            if form.password.data != form.password_confirm.data:
                flash('Password and confirm password does not match', 'error')
                return False
            try:
                user = User() # Added this line to create the user object since its required to create the passworduser object
                model = self.model(user)
                form.populate_obj(model)
                self.session.add(model)
                self._on_model_change(form, model, True)
                self.session.commit()
            except Exception as ex:
                if not self.handle_view_exception(ex):
                    flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                    logging.exception('Failed to create record.')

                self.session.rollback()

                return False
            else:
                self.after_model_change(form, model, True)

            return model
        else:
            flash('Failed to create user. Only admin users can create new user', 'error')
            return False

    def update_model(self, form, model):
        if form.password.data == form.password_confirm.data:
            logging.info("UserManagementModelView.update_model(form=" + str(form) + ", model=" + str(model) + ")")
            return super(UserManagementModelView, self).update_model(form, model)
        else:
            flash('Password and confirm password does not match', 'error')

    def delete_model(self, model):
        if is_super_user(self):
            logging.info("UserManagementModelView.delete_model(model=" + str(model) + ")")
            return super(UserManagementModelView, self).delete_model(model)
        else:
            flash('Failed to delete user. Only admin users can delete a user.', 'error')


# Creating View to be used by Plugin
user_management = UserManagementModelView(PasswordUser, Session, name="User Management", category="Admin", url="usermanagement")

# Creating Blueprint
user_management_bp = Blueprint(
    "user_management_bp",
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/'
)


# Creating the UserManagementPlugin which extends the AirflowPlugin so its imported into Airflow
class UserManagementPlugin(AirflowPlugin):
    name = "user_management"
    operators = []
    flask_blueprints = [user_management_bp]
    hooks = []
    executors = []
    admin_views = [user_management]
    menu_links = []
