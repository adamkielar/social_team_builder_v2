# social_team_builder


# Installation:

git clone

Docker: 
- docker build . 
- docker-compose build 
- docker-compose up 
- to access postgresql database: docker-compose exec db psql --username=postgres --dbname=postgres

Virtualenv: 
- python3 -m venv env 
- source ./env/bin/activate 
- pip install --upgrade pip && pip install -r requirements.txt 
- python manage.py makemigrations accounts && python manage.py makemigrations accounts && python manage.py migrate 
- python manage.py runserver 0.0.0.0:8001 ( important to use 8001 port so allauth package will work)

Sample data: User need to add Main Skills and Other Skills (in django admin for example) to create User Profile
Project includes database, sqlite, with sample data.
Django admin:
email: root@test.pl
password: Testing098

To load data to empty sqlite database:

python manage.py loaddata accounts_sample.json
python manage.py loaddata projects_sample.json
