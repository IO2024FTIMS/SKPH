# SKPH (IO_2024)

### Setup
1. Create `.env` file in the `docker/database` directory with the selected credentials and settings to your local database.

```conf
DB_NAME="<db_name>"
DB_USER="<user_name>"
DB_PASSWORD="<password>"
DB_PORT="<port>"
```

2. Set the `DATABASE_URI` environment variable to match with the `.env` file.
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

## Working in This Repository

To merge changes into the `main` branch, please ensure the following requirements are met:

- **Branch Naming**: Follow these naming conventions:
    - `feature/<name_of_the_feature>` for new features
    - `fix/<name_of_the_fix>` for bug fixes

- **CI Checks**: All CI checks must pass, including:
    - Static analysis with Pylint and Flake8 (errors can be suppressed if necessary)
    - Successful execution of unit tests
    - Running the Flask application

- **Pull Request Reviews**: The Pull Request requires two approvals, with at least one from a code owner.

- **Branch Synchronization**: Ensure the branch is up-to-date with `main`.

### Working with `epic` Branches for Larger Features

For more complex functionality that may require multiple `feature/**` branches:

- Create an `epic/<name_of_the_epic>` branch to develop related features.
- Develop smaller `feature/**` branches and merge them into the `epic` branch without worrying about the CI checks and branch protection rules.
- When the `epic` branch is ready for integration into `main`, ensure it meets all the above requirements.
