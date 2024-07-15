Polaris Assignment 

To run project create a virtual env

Use - python -m venv venv

Now activate the virtual env

Now install the dependency using - pip install -r requirement.txt

we are using postgres

please create an .env file with your postgres db creds

migrate the db using - python manage.py migrate

now run the server on any port (change in postman collection according to port) - python manage.py runserver

some todos to scale this we can make this in microservice architecture  

we can add caching as its very read heavy application 

we add load balancer as well 
