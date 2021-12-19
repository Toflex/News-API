# News API
This project allows viewers to read latest news in technology. 
Contents are been updated periodically from the Hacker News API, but can also be added via a public API, documentation for the Public APIs can be found on

`/docs`

# Getting started

Download and install python v3.10

Run the below commands:

`python3 -m venv ./env`

`source env/bin/activate`

`pip install -r requirements.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`


# Project Config
The number of news fetched from Hacker news API can be set in the settings.py file "HACKER_NEWS_RANGE", the default is 100.
