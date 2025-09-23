# Task 1: Multi-Tenant Invitation System
This project was implemented following the file [Practical_Task](https://github.com/rkpust/multitenant-project/blob/master/multitenant/Practical_Task.docx.pdf)

## How To Setup The Project
By following the given below instruction, you can easily setup the project.
### Step 1
Create a vitual environment and activate it (Windows).
```python
python -m venv venv
venv\Scripts\activate
```

### Step 2
Clone the project from GitHub.
```python
git clone https://github.com/rkpust/multitenant-project.git
```
And change directory in `manage.py` level.

### Step 3
Install the required packages from `requirements.txt`
```python
pip install -r requirements.txt
```
### Step 4
Create Database (recomnded `PostgreSQL`) and rename `.env.example` to `.env` and set value of variable.

### Step 5
Go to the project directory and run those commands to migrate.
```bash
python manage.py makemigrations
python manage.py migrate
```
### Step 6
Create a superuser by following the command to gain access to the admin interface.
```bash
python manage.py createsuperuser
```


### Step 7
Run the server by following the command.
```bash
python manage.py runserver
```

### Step 8
Go to the `/admin` path, login with the previously created superuser credentials, and create Tenant.
### Step 9
Open bash terminal and test the `API`. Let your server `127.0.0.1:8000`. Now hit `/login` endpoint and get access token. Note that access token lifetime is one hour.
#### POST `/login/`
```curl
curl --location 'http://127.0.0.1:8000/login/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "rezaul",
    "password": "12345678"
}'
```

##### `Note` You can get and update the token by following the provided `API` endpoint.
```bash
POST /api/token/
POST /api/token/refresh/
```
By directly accessing the API in the browser.

[http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
<br>
[http://127.0.0.1:8000/api/token/](http://127.0.0.1:8000/api/token/)
<br>
[http://127.0.0.1:8000/api/token/refresh/](http://127.0.0.1:8000/api/token/refresh/)


#### Ouput
```json
{
"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2NTc2NTQyLCJpYXQiOjE3NTY1NzI5NDIsImp0aSI6IjNmYTQ3NGYyNWRjYjQyMjA4NTI0ZjVlNTQxZjY2YmVlIiwidXNlcl9pZCI6IjIifQ.xDLUpyaodfzSpKS2ZSZVQGau1kdvni7zdUjDSuGwd7E",
"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NjY1OTM0MiwiaWF0IjoxNzU2NTcyOTQyLCJqdGkiOiI4NmFjN2M3MGZlYjI0N2U3OTc1ODQ3NGJlZjk4NDU0OCIsInVzZXJfaWQiOiIyIn0.Noed7NFFaFWV1lY5436xUfEa02_WTjp0rxspQogYjU4"
}
```

#### POST `/invite/`
```bash
curl --location 'http://127.0.0.1:8000/invite/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4NjU1NjU1LCJpYXQiOjE3NTg2NTIwNTUsImp0aSI6ImFkMDkxNzU2ZmNjZDQ4OWFiZGYzYzM2MjY3NzlmYTI1IiwidXNlcl9pZCI6IjEifQ.v421tMRhTvK1iQVzio5xspHciHv448jWNeQIOZMlD0w' \
--header 'Content-Type: application/json' \
--data-raw '{
    "tenant": 1,
    "name": "Rezaul Karim",
    "email": "rezaul.cse.pust17@gmail.com"
}'
```

#### Ouput
```json
{
    "id": 20,
    "tenant": 1,
    "name": "Rezaul Karim",
    "email": "rezaul.cse.pust17@gmail.com",
    "status": "PENDING",
    "token": "c2dd86de-1ad3-4c9f-b9c4-f3350025341a",
    "metadata": "{\"ip\": \"127.0.0.1\", \"user_agent\": \"PostmanRuntime/7.43.0\"}"
}
```
#### POST `accept/<uuid:token>/`
```bash
curl --location 'http://127.0.0.1:8000/accept/c2dd86de-1ad3-4c9f-b9c4-f3350025341a/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "rezaul",
    "password": "12345678"
}'
```

#### Ouput
```json
{"message": "Invitation accepted successfully."}
```
#### POST `cancel/<uuid:token>/`
```bash
curl --location 'http://127.0.0.1:8000/cancel/c2dd86de-1ad3-4c9f-b9c4-f3350025341a/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "rezaul",
    "password": "12345678"
}'
```

#### Ouput
```json
{"message": "Invitation cancelled."}
```


### Step 10
Clean up expired tokens by running a custom command.
```python
python manage.py expire_invitations
```

### Step 11
If there is any need, please ping me. ❤️

<b>Md. Rezaul Karim</b>
<br>
+8801751471885
<br>
<a href="mailto:rezaul.cse.pust17@gmail.com">rezaul.cse.pust17@gmail.com</a>
<br>
https://sites.google.com/view/rkpust