- [Company challenge](#company-challenge)
- [Running the application](#running-the-application)
  - [With `docker-compose`](#with-docker-compose)
  - [Locally with poetry](#locally-with-poetry)

# Company challenge

The challenge is described in the [CHALLENGE.md](CHALLENGE.md) file. This is the solution proposed by me, Felipe Lima.

# Running the application
> For both modes ([`docker-compose`](#with-docker-compose) and [`locally`](#locally-with-poetry)) you need to create a `dev.env` file following the template given [here](configurations/env_template) before running the application.

## With `docker-compose`
1. Run:
   ```shell
   docker-compose up -d
   ```
2. Execute the migrations with:
   ```shell
   docker-compose exec backend python manage.py migrate
   ```
3. You are good to go. Just type on your browser `localhost:8000/docs/` and you will be shown the `OpenAPI` specifications for the entire API.
## Locally with poetry
This is messier than the [`docker-compose`](#with-docker-compose) approach. You are encouraged to use that approach. With this being said:

1. You need to have [poetry]() installed before running backend service.
2. You need to have a PostgreSQL and Redis servers configured to the values you defined in your `dev.env` file.
3. Run the following commands:
    ```shell
    # I'm assuming you have the db (PostgreSQL) and redis services up and running before executing this command.
    env $(grep -v '^#' configurations/dev.env | xargs) poetry run python manage.py migrate
    env $(grep -v '^#' configurations/dev.env | xargs) poetry run python manage.py runserver
    ```
4. Start the `celery-beat` worker with:
   ```shell
   env $(grep -v '^#' configurations/dev.env | xargs) poetry run celery --app core beat --loglevel=INFO
   ```
5. You are good to go. Just type on your browser `localhost:8000/docs/` and you will be shown the `OpenAPI` specifications for the entire API.