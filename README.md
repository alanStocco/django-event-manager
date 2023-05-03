# Django Rest Framework Event Manager App.

## How To Setup On Linux
1. Clone This Project `git clone https://github.com/alanStocco/django-event-manager`
2. Go to Project Directory `cd django-event-manager`
3. Create a Virtual Environment `python3 -m venv env`
4. Activate Virtual Environment `source env/bin/activate`
5. Install Requirements Package `pip install -r requirements.txt`
6. Go to base Directory `cd base`
6. Migrate Database `python manage.py migrate`
7. Create Super User `python manage.py createsuperuser`
8. Finally Run The Project `python manage.py runserver`