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
