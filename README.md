
# Ticketing Tool using Django 

A web-based ticketing tool where users can create tickets, assign them to engineers, and engineers can manage ticket details including adding comments and updating ticket status

## Features
    1. Login and Register for Engineers, superuser and users
    2. Ticket list visible to everyone according to their role, engineer sees all tickets assigned to them, user see all tickets created by them and superuser i.e admin sees all tickets.
    3. Creating new tickets.
    4. View ticket details.
    5. Updating ticket status.
    6. Adding comments to tickets.

## Project Setup
To use this project to your own machine follow this steps
### Clone repository from github
First of all, clone this repository using this command
    https://github.com/vaishnavibhujbal23/Ticketing-Tool.git

### Install the dependencies
Install the requirements of it from the file using this command :
pip install -r requirements.txt

### Create Database 
sqlite3 setup for project is done. Apply migrations using this command : python manage.py migrate

### Run this project
Let's run the development server : python manage.py runserver

#### Now you’re project is already run into a development server.

Just click this link : http://127.0.0.1:8000/

## Files and Directories

### Main Directory :
ticketingtool - Main application directory.

    settings.py - All Project Settings File
    urls.py - All Project url paths

templates - Holds all html files.

    registration - login.html and register.html
    ticket - 1. base.html
             2. create_ticket.html
             3. manage_tickets.html
             4. ticket_detail.html
             5. ticket_list.html


ticket -Sub-application Directory.

    urls.py - All ticket url paths
    views.py - Contains all view functions for ticket 
    models.py - Contains 3 classes User, Ticket and Comment
    forms.py - Contains 3 forms for User creation, ticket creation and comment creation 