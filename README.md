# airflow-user-management-plugin

## Description

A plugin to Apache Airflow (Documentation: https://pythonhosted.org/airflow/, Source Code: https://github.com/apache/incubator-airflow) to provide an interface where you can add a PasswordUser to Airflow and manage

## How do Deploy

1. Copy the user_management_plugin.py file into the Airflow Plugins directory

    * The Airflow Plugins Directory is defined in the airflow.cfg file as the variable "plugins_folder"
    
    * The Airflow Plugins Directory is, by default, ${AIRFLOW_HOME}/plugins
    
    * You may have to create the Airflow Plugins Directory folder as it is not created by default
    
    * quick way of doing this:
    
        $ cd {AIRFLOW_PLUGINS_FOLDER}
        $ wget https://raw.githubusercontent.com/teamclairvoyant/airflow-user-management-plugin/master/user_management_plugin.py
 
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