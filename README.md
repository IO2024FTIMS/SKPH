# IO_2024

### Setup
1. Create `.env` file in the `docker` directory with the selected credentials to your local database.

```conf
POSTGRES_DB="<db_name>"
POSTGRES_USER="<user_name>"
POSTGRES_PASSWORD="<password>"
```

2. Set the `DATABASE_URI` environment variable to match the `.env` file.
> Note: Restarting your terminal/IDE may be required for the change to take place.
```sh
DATABASE_URI=postgresql+psycopg2://${user_name}:${password}@localhost:54329/${db_name}
```

3. Run the docker container with database
```sh
docker compose -f docker/database/docker-compose.yml up -d
```

### Running the application
```sh
flask run
```
