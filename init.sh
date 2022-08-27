#!/bin/bash

sudo docker-compose run web django-admin startproject website .
sudo docker-compose run web python manage.py startapp credentials