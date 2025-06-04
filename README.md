# ALEMBIC CLI OPERATIONS

## Initialize alembic

- Command -> `alembic init alembic`

## Generate a version

- Command -> `alembic revision --autogenerate -m "create user table"`

## Commit the version changes to the database

- Command -> `alembic upgrade head`
