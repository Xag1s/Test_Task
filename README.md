# Test Task

## Installation
### Clone the Repository
Clone this repository to your local machine:
```commandline
git clone https://github.com/stepankindrat/Test_Task.git
```
### Create a `.env` file
Create a .env file in the root directory, example of `.env` file:
```
JWT_SECRET_KEY="default_secret_key"
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db
```
## Build application
Run the following command to build and start the containers:
```commandline
docker compose build 
docker compose up -d
```
Test that the container is running by executing `docker-compose ps`.

## Create tables and load data
Run the following command to set up the database:
```commandline
docker compose exec app python load_data.py
```
After executing the command, four articles and three users will be created with the following user data::
```commandline
username: User-Admin
password: admin
role: Admin

username: User-Editor
password: editor
role: Editor

username: User-Viewer
password: viewer
role: Viewer
```

## Run tests
To execute tests using pytest, run:
```commandline
docker compose exec app pytest
```

## Custom commands
Run following command to create new user
```commandline
docker compose exec app flask create-user <username> <password> <role>
```
Run following command to clean up the database
```commandline
docker compose exec app flask reset-db
```

