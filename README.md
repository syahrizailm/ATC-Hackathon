# ATC-Hackathon
Prototype for Catalyst: End-to-End IT Talent Solution. Company can get talent easier and cheaper in our database. Student can upskill themselves and wait for job invitation, skipping exhausting job hunting process

### Existing feature
* Add talent to database
* Find talent in database based on several conditions

### How to open production
* Site for student to enter their portfolio: https://atc-hackathon-aria.herokuapp.com
* Site for company to find talent: https://atc-hackathon-aria.herokuapp.com/business

### How to install in local
* Create virtual env with python -m venv atc-venv
* Input database in .env file with format MONGO_CONNECTION="Your Connection URI"
* Run pip install -r requirements.txt

### How to run in local
* Run python app.py

### Folder Description
* app.py: main file
* database.py: connection to MongoDB
* pages: Interface
* layout: layout that is used in pages file