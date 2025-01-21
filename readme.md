# Auth Service for user authentication

## Software Installation
Install following software:
```
Python 3
PostgreSQL 
Redis
```

## App Installation
Prepare local POSTGRES database
```bash
#
sudo -u postgres psql -c "CREATE DATABASE users_db;"
sudo -u postgres psql -c "CREATE USER db_user WITH PASSWORD 'db_pass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE users_db to db_user;"

#install libraries
pip install -r constraints.txt

#run migrations
alembic upgrade head
```

For testing purposes create 2 records in Users table
```
INSERT INTO users VALUES('admin', 'hash', null, 'admin@gmail.com', 'ADMIN', '970f7694-bac9-4334-aa1a-17b38158db57');
INSERT INTO users VALUES('user1', 'hash1', null, 'user1@gmail.com', 'USER', '10333888-e47c-4e2b-b996-b99a956e5ecd');
```