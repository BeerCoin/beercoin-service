beercoin-service
================

The awesome beercoin webservice


setup
-----

$ virtualenv . 
$ source bin/activate
$ bin/pip install -r requirements.txt

# In the directory where the settings.py is located
$ touch settings_local.py

# South Migrate
$ python manage.py migrate beercoin

# After a migrate you MUST fix the permissions
$ python manage.py check_permissions

