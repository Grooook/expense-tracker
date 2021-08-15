# Expence tracker
Web application to monitor your expenses/incomes money.

## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Functionality supported by the application](#functionality-supported-by-the-application)

### Technologies
Project is created with:
* Django: 3.2.6
* django-bootstrap-v5: 1.0.5
* django-crispy-forms: 1.12.0
* matplotlib: 3.4.3
* numpy: 1.21.1

### Setup

First clone this repository:
```sh
...> git clone https://github.com/Grooook/expense-tracker.git
...> cd expense-tracker
```

Create venv and activate it:
```sh
...> python -m venv env
...> env\Scripts\activate.bat
```

Then install the dependencies:
```sh
(env)...> cd expense-tracker
(env)...> pip install -r requirements.txt
```

Make migrations and run server:
```sh
(env)...> python manage.py migrate
(env)...> python manage.py runserver
```

And navigate to http://127.0.0.1:8000/accounts/registration/


### Functionality supported by the application

Web application supports registration, authorization and user deletion.

> #### Creating transactions
> <img src="https://github.com/Grooook/expense-tracker/blob/master/media/add_transaction.gif"/>


> #### Edition transactions
> <img src="https://github.com/Grooook/expense-tracker/blob/master/media/edit_transaction.gif"/>


> #### Delete transactions
> <img src="https://github.com/Grooook/expense-tracker/blob/master/media/delete_transaction.gif"/>


> #### Expense/Income view fetch across all categories
> <img src="https://github.com/Grooook/expense-tracker/blob/master/media/categories.gif"/>


> #### Profile statisctics
> <img src="https://github.com/Grooook/expense-tracker/blob/master/media/profile_statistics.gif"/>
