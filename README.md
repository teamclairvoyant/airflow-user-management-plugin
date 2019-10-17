# airflow-user-management-plugin

## Description

A plugin to Apache Airflow (Documentation: https://airflow.apache.org/, Source Code: https://github.com/apache/airflow) to provide an interface where you can add a PasswordUser to Airflow and manage

### RBAC Support
If you are using the Airflow versions 1.10.x and higher then this plugin is useful only when RBAC feature is disabled. 
You can check the `rbac` setting in `airflow.cfg` config file under `webserver` category. When RBAC feature is enabled 
you can manage users directly from the `Security` menu provided by Airflow UI.   

**Note:** Once you enable the RBAC support, it will create new set of Database Tables. So, you need to manually 
migrate your existing users from `users` table to the new table `ab_users`. While migrating you need to specify 
the role for each user. Please check [Create User](https://airflow.apache.org/cli.html#create_user) for more details.

## How do Deploy

1. Copy the user_management_plugin.py file into the Airflow Plugins directory

    * The Airflow Plugins Directory is defined in the airflow.cfg file as the variable "plugins_folder"
    
    * The Airflow Plugins Directory is, by default, ${AIRFLOW_HOME}/plugins
    
    * You may have to create the Airflow Plugins Directory folder as it is not created by default
    
    * quick way of doing this:
    ```bash
        $ cd {AIRFLOW_PLUGINS_FOLDER}
        $ wget https://raw.githubusercontent.com/teamclairvoyant/airflow-user-management-plugin/master/plugins/user_management_plugin.py
     ```
 
2. Restart the Airflow Services

3. Your done!

## How to Use

Once you've restarted the Web Application, you should now see a new Tab: Admin -> User Management. From here, you can create new users and update or delete existing ones.

## Configuration
* This plugin requires that you already have one Airflow user setup.  Please refer http://airflow.apache.org/security.html#password to know how to setup Airflow user.
* Only Admin Users can create/delete other users.

* Add the following configuration in the airflow.cfg file for versions < 2.0

        [user_management_plugin]
        #provide comma separated list of admin users
        #Ex: admin_users=admin,airflow
        admin_users=airflow
        
* For versions >= 2.0 you need to make sure the `superuser` attribute is set to `True` for the Airflow User. Please refer http://airflow.apache.org/_api/airflow/models/index.html#airflow.models.User for details.

**Note:** `superuser` flag in the create/edit user form will be effective only from version >= 2.0

####Known issues
* **Issue**:  When you run the plugin with SQLAlchemy versions >= 1.2.x on Airflow versions < 1.10.x then you might run into the following `AttributeError` issue
    
        [2019-03-19 11:07:52,979] {user_management_plugin.py:71} INFO - UserManagementModelView.create_model(form=<flask_admin.contrib.sqla.form.PasswordUserForm object at 0x7fbf3362af90>)
        [2019-03-19 11:07:52,979] {user_management_plugin.py:82} ERROR - Failed to create record.
        Traceback (most recent call last):
         File "/home/dillip/airflow/plugins/user_management_plugin.py", line 75, in create_model
           form.populate_obj(model)
         File "/home/dillip/.local/lib/python2.7/site-packages/wtforms/form.py", line 96, in populate_obj
           field.populate_obj(obj, name)
         File "/home/dillip/.local/lib/python2.7/site-packages/wtforms/fields/core.py", line 330, in populate_obj
           setattr(obj, name, self.data)
         File "/home/dillip/.local/lib/python2.7/site-packages/sqlalchemy/ext/hybrid.py", line 899, in __set__
           raise AttributeError("can't set attribute")
        AttributeError: can't set attribute 
              
    **Resolution**: Please use SQLAlchemy versions <= 1.1.18 to resolve the issue.
