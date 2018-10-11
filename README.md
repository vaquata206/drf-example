# drf-example
## Requirements
* Python 3.6.*
* Django 2.0.*
## Installation
Open terminal in root dir and run command line bellow
```
# Create a virtualenv to isolate our package dependencies locally
virtualenv env
source env/bin/activate

# Install Django and Django REST framework into the virtualenv
pip3 install django
pip3 install django djangorestframework django-filter

# Install Django REST framework jwt
pip3 install djangorestframework-jwt
```
Install djangorestframework and djangorestframework-jwt


## Getting Started
Open terminal in root dir and run command lines bellow
```
source env/bin/activate
cd drfexample
python3 manage.py runserver
```
## Running the test
Open terminal in root dir and run command lines bellow
```
source env/bin/activate
cd drfexample
python3 manage.py test
```
