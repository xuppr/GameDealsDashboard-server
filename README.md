Game Deals Dashboard - server
=============================

This app is running on Heroku.

How to run
----------

Clone the project, cd into the project folder and run the following commands:

```
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python3 manage.py migrate
  python3 manage.py fetchdeals
  python3 manage.py runserver
  
```

How to test
-----------

```
  python3 manage.py test
```
