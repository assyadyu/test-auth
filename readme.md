# Auth Service for basic user authentication

Generates and validates access tokens if provided credentials are correct

## Software Installation
Install following software:
```
Python 3
PostgreSQL 
```

## App Installation
Prepare local POSTGRES database users_db
```bash
#
sudo -u postgres psql -c "CREATE DATABASE users_db;"
sudo -u postgres psql -c "CREATE USER db_user WITH PASSWORD 'db_pass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE users_db to db_user;"
```
Set environment variables (see app/common/settings.py)

and run
```bash
# install libraries
pip install -r constraints.txt

# run migrations
alembic upgrade head

# run server -- make sure auth server is running
uvicorn app.main:app --port 3000 --reload 

# Swagger UI
http://127.0.0.1:3000/docs#/

```

Option 2. Using Docker

Note 1: First build container from test-orders repo, it contains shared network 
```bash
docker compose up --build
# run with testing profile that executes tests
docker compose --profile testing up --build

# Swagger UI
http://0.0.0.0:3000/docs#/
```

Note 2: No tests since there is no business logic and operations are trivial