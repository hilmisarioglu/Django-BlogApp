# CREATING VIRTUAL ENVIRONMENT

# windows
py -m venv env
# windows other option
python -m venv env

# ACTIVATING ENVIRONMENT
# windows
source ./env/Scripts/activate

# PACKAGE INSTALLATION
# if pip does not work try pip3 in linux/Mac OS
pip install django
# alternatively python -m pip install django
pip install python-decouple
django-admin --version
django-admin startproject main .
```

go to settings.py, make amendments below
```python
from decouple import config
SECRET_KEY = config('SECRET_KEY')
go to terminal
```bash
py manage.py migrate
py manage.py runserver
```
click the link with CTRL key pressed in the terminal and see django rocket.
go to terminal, stop project, add app
```
py manage.py startapp app


INSTALLED_APPS = [
    'app',
]

go to settings.py and add 'main' app to installed apps and add below lines
```python
import os
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

