# social_team_builder
TreeHouse Project 12

1. Users - this app will take care of user auth and profiles
    - routes (signup, login, edit profile, logout)
    - profile (Extend user model, avatar, user skills, permission to create project )
    - email verification after signup
    - Markdown in "about me" profile, project description, position description
    - list of all skills not only selected
    - profile should list project user in involved with
    - show project that need user skill set

2. Projects (name, description, positions, skills)
    - position should be filled after accept (no available for click)
    - length of involvement

3. Community (members(see,approve,reject))  CommunityMember
    - filter user status (approved, denied, undecided)
    approve or denied from the list of applicants

Members notification

4. Search functionality(projects by title and descriptions)

#Installation:

git clone

Docker: a) docker build . b) docker-compose build c) docker-compose up d) to access postgresql database: docker-compose exec db psql --username=postgres --dbname=postgres

Virtualenv: a) python3 -m venv env b) source ./env/bin/activate c) pip install --upgrade pip && pip install -r requirements.txt d) python manage.py migrate e) python pugorugh/scripts/data_import.py #load sample data f) python manage.py runserver 0.0.0.0:8001 ( importent to use 8001 port so alluth package will work)

Sample data: User need to add Main Skills and Other Skills (in django admin for example) to create User Profile