# ATS - Applicants Tracking System

## API v1 root url:

http://localhost:9999/api/v1

## Admin credentials:
#### login: admin
#### password: admin

## Setup DB
1. Create DB in your PostgreSQL.
Then put DB url to `SQLALCHEMY_DATABASE_URL` variable in `database/db.py`

2. ##### To setup DB - run:
    ```bash
    make setup_db
    ```

## Run app

```bash
make run
```

## Run app for development purposes with auto-reload

```bash
make run_dev
```

## Project

https://github.com/luchkavl/ATS
