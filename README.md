# Python Chat API + Web Client

A Python/Django REST API to manage a chat application. 
Also, there is a sample Web Client to consume the API endpoint.

## Chat API Features

* Manage messages, senders and recipients
* Built-in "Echo" auto-responder Service, extensible to new services
* Configured to be deployed in Heroku
* Python modules: 
  * `django`: Full featured Web framework
  * `gunicorn`: Python WSGI HTTP Server for UNIX
  * `django_heroku`: Heroku module for deployment integration

##  Chat Web Client Features

* Web based Front-end static client
* Google Login integration
* Send and Receive messages to any contact by email. 
* Web technologies:
  * Vue.js: JavaScript Framework for web applications
  * Vuetify: Material Design UI Component Framework
  * gapi : Google API client for Javascript
  * web workers: To receive and send API request in a separate process
  

## Development

### Install python packages

`pip install -r requirements.txt`


### Prepare database

Create database schema

`python manage.py migrate`

Create a super user

`python manage.py createsuperuser`



### Run the web service (Debug mode)

To run with DEBUG activated:

`export DEBUG=1`

`python manage.py runserver`

### Run the web service (Production mode)

To run with DEBUG disabled:

`unset DEBUG`

`python manage.py collectstatic`

`python manage.py runserver`

### Access the web service

Go to http://localhost:8000/ for the main site

Go to http://localhost:8000/admin/ for the administrator interface, using your previously created super user.



## Deployment to Heroku

### Install Heroku client

This command line interface (CLI) helps to do some tasks related to Heroku. 

You can install this tool following [the official guide](https://devcenter.heroku.com/articles/heroku-cli#download-and-install). 

The main steps are:

1.- For MacOS, install Homebrew and run
`brew install heroku/brew/heroku`

2.- In Ubuntu/Debian based systems, install SnapCraftand run
`sudo snap install --classic heroku`

3.- For windows, download and execute the installer.

### Register your application in Heroku

1.- Create an account in Heroku.com to login (https://signup.heroku.com/)
2.- After registation, go to https://dashboard.heroku.com/
3.- Create a new application using the button [Add] (https://dashboard.heroku.com/new-app)

### Login to Heroku

You need an accout in Heroku.com to login.

`heroku login [--interactive]`

### Asociate your repository with Heroku

Use the **app name** you previously registered in Heroku

`heroku git:remote -a your-app-name`

### Deploy your application

`git push heroku master`

At the **end of the deployment** log you will find the administrator password created:

`
remote: Admin created with pass [Admin.56734564]
`

### Access the Heroku application

Go to `http://your-app.herokuapp.com/` for the main site

Go to `http://your-app.herokuapp.com/admin/` for the administrator interface. User is 'admin' and the password is created during the first deployment.







