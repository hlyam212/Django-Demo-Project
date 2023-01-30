# Django-Demo-Project

## Simple Work Steps

### 1.Create Project
django-admin startproject django_REST

### 2.Create App
python manage.py startapp customer

### 3.Define Model & Create Table
3.1 django_REST\customer\models.py  
3.2 Create a dbtest in postgresq  
python manage.py makemigrations  
python manage.py migrate  
[Note]Reset an App Database Tables in Django : python manage.py migrate customer zero

### 4.Setting DB Connection
django_REST\django_REST\settings.py : DATABASES  
To run this demo, needs to change the PASSWORD to your local setting in settings.py

### 5.Define View & actions
django_REST\customer\views.py

### 6.Run application
python manage.py runserver

### 7.Test with Postman


