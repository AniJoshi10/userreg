# User Registration

# 1. Requirements

-> (A detailed list is specified in /requirements.txt)
  + python 3.5 or higher
  + django 3 or higher
  + django-mongoengine
  + bcrypt
  
# 2. Setup

-> Install virtualenv
  + (Using pip3) $ pip3 install virtualenv
  
-> Activate virtualenv
  + $ virtualenv <prjname>
  + $ cd <prjname>/Scripts
  + $ bash activate.sh [OR] $ activate.bat
  
-> Install python libraries from requirements.txt
  + $ pip3 install -r requirements.txt
  
-> Changes to <prjname>/myprj/myprj/settings.py
  + ALLOWED_HOSTS = [*]
  + STATIC_ROOT = os.path.join(BASE_DIR, 'static')
  + DEBUG = True
  + MONGODB_DATABASES = { *make suitable changes to connection uri,
                          host, username and password to connect to your
                          MongoDB database collection* }
  
# 3. Run django application

-> Make migrations
  + $ cd myprj
  + $ python manage.py makemigrations
  + $ python manage.py migrate
  
-> Run server
  + $ python manage.py runserver
  
[ Now visit the url as specified in the terminal. ]
  
  
