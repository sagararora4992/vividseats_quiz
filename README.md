vivid_seat_assignment
=====================

Getting Started
---------------

- Change directory to the cloned repository given below command.
    - cd vividseats_quiz

- Run the below commands for creating mysql docker image:
- docker build -t my-mysql .
- docker run -d -p 5432:3306 --name my-mysql -e MYSQL_ROOT_PASSWORD=supersecret my-mysql

- Create a Python virtual environment.
    - python3 -m venv env

- Upgrade packaging tools.
    - env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.
    - env/bin/pip install -e ".[testing]"

- Activate the virtual ENV
    - source env/bin/activate

- Initialize and upgrade the database using Alembic.
    - pip install pymysql
    - pip install cryptography
    - Generate your first revision.
    - alembic -c development.ini revision --autogenerate -m "init"


- Load default data into the database using a script.
    - pip install pyramid_jinja2
    -initialize_vivd_project_db development.ini

- Run your project.
  - pserve development.ini



After this to test the api:
for first use case:
http://localhost:6543/available_tickets?event_id=107 put this url in browser

for second use case (new ticket) POST advisable to use postman
url will be like below
http://localhost:6543/new_ticket
and in body in form data we can give below values:
event_id, section, rownum, seat, price, seller_id, status Please provide value of all these columns

for 3rd case PUT, url will be like this 
http://localhost:6543/update_ticket
event_id, section, rownum, seat, price, seller_id, status please provide all the values of these columns

for 4th case get best ticke(GET)
url will be like this 
http://localhost:6543/best_ticket?event_id=107
just paste this in browser you will get the result.
