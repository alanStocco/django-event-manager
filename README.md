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


 The task consists in creating a Rest API using Django rest framework https://www.django-rest-framework.org/to create an Event manager app. 
 It should allow users to create a personal account, log in, and create, edit, fetch, and register to attend events. 
 Each event should have at least a name, a description, a start date and end date and a list of attendees.

 
Features:
 

- Users must be able to register an account

- Users must be able to log in into their account

- A system of token rotation must be implemented. For this the API needs to provide a user with access_token and a refresh_token, as well as a way to refresh and validate the access_token. The lifetime of the access_token should be 1 hour and the lifetime of the refresh_token 1 day

- Users must be able to create events in the app's database (slqlite)

- Users must be able to see the list of events they have created

- Users must be able to see a list of all events

- Users must be able to edit the events they have created but not the ones created by other users

- Users must be able to register to an event or un-register. This can only be done in future events and not in past events.

- Add logic to manage an event capacity: if event reaches maximum number of registered attendees, an error should be returned to a user trying to register

- Add some  filtering to endpoints retrieving events (e.g. date , type, status, past events, future events, etc)


-- (26/05/23)In progress

- Documentation of your code. Google style docstring https://google.github.io/styleguide/pyguide.html

- API docs swagger TODO finish

- Tests TODO unit_test, pytest? What else?

- Create a frontend to consume the API TODO