# ClubApplication

About this project
-------------------
This web application is used to monitor club member data, create weekly problem solving challenges and organise events in a college.

Technologies used
-----------------
This is a web application developed with Django, PostgreSQL for backend developemnt and HTML, CSS, Bootstrap, JavaScript for frontend web design.

##### How to setup project?
1. Setup a database 
-> open settings.py and setup a database connection
2. Create a super user 
cmd: py manage.py createsuperuser
3. Run server
cmd: py manage.py runserver
4. Add a student data
-> open http://127.0.0.1:8000/admin/login/?next=/admin/ on browser and login with superuser credentials
-> open Members and add members
5. Add a co-ordinator who monitors Members 
-> open http://127.0.0.1:8000/admin/login/?next=/admin/ on brower and login with superuser credentials
-> open Admins and add admins

##### How to use this project?
1. Create an account 
-> open http://127.0.0.1:8000/signup/ on browser and create but admins have to accept your request.
2. Login for members
-> open http://127.0.0.1:8000/login/ on broweser and explore the feaures available.
3. Login for admins
-> open http://127.0.0.1:8000/administrator/ on browser and explore the feature available