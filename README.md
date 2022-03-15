# Test-Shorty
Python 3 Flask web application to generate short URLs.

### Requirements
* Python 3
* SQLite 
* Flask
* Flask-RESTful

requirements.txt:
```shell
alembic==1.7.7
aniso8601==9.0.1
arrow==1.2.2
click==8.0.4
Flask==2.0.3
Flask-Migrate==3.1.0
Flask-RESTful==0.3.9
Flask-SQLAlchemy==2.5.1
Flask-WTF==1.0.0
greenlet==1.1.2
gunicorn==20.1.0
importlib-metadata==4.11.3
importlib-resources==5.4.0
itsdangerous==2.1.1
Jinja2==3.0.3
Mako==1.2.0
MarkupSafe==2.1.0
python-dateutil==2.8.2
python-decouple==3.6
pytz==2021.3
six==1.16.0
SQLAlchemy==1.4.32
times==0.7
Werkzeug==2.0.3
WTForms==3.0.1
zipp==3.7.0
```

### Installation
Requirements:
```
pip install -r requirements.txt
```
Database:
```
flask db init
```
```
flask db migrate
```
```
flask db upgrade
```

### How to use App
* Run file main.py 

* Enter in the field (URL) your link want it to be shorten

* Enter in the field (Life Time) how long days the link should exist

* Submit

* The link which will be created and will be your short link

If you want custom id Enter in the field (Custom id)

### How to use Api

* Run file main.py 

How GET all urls?

* Send a GET request to endpoint
```
http://127.0.0.1:5000/list_urls
```
How POST urls with API?

* Send a POST request to endpoint
```
http://127.0.0.1:5000/create_urls
```
With body request Example 

```
{
   "original_url": "https://www.youtube.com/",
   "short_id": "",
   "time_life": "1"
}
```
If you want custom id Enter in the field (Custom id)
