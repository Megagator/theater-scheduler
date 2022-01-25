# Theater Scheduler

A Django app to schedule movies during in many theaters across many days


## Environment
If you don't already have a Python3 or a virtualenv with Django 4.x installed, follow these instructions to get up and running in a virtual shell environment: [https://docs.djangoproject.com/en/4.0/topics/install/](https://docs.djangoproject.com/en/4.0/topics/install/)

TL;DR, use
- `python3 -m venv ~/.virtualenvs/theater_scheduler` to create your venv
- `source ~/.virtualenvs/theater_scheduler/bin/activate` to activate the environment
- `python -m pip install Django` to install Django

_note: you can run `deactivate` to exit this virtual environment, or just close your shell instance_


## Install

- Download and extract this repo, or git clone it, into a working directory.
- This app uses SQLite, so no outside datastore servers need to be running. Simply run the migration with in the working directory's root: `python manage.py migrate`
- To skip having to create your own theaters and movies, you can load the fixture data with: `python manage.py loaddata movies theaters`
- If you would like to explore the Django admin site, create a user: `python manage.py createsuperuser` and follow the prompts


## Run
`python manage.py runserver`

Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the client.

Navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin) and login with your username and password from the install to view the admin site.