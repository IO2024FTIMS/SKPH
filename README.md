# SKPH (IO_2024)

## [Web app](https://skph-io-ftims-dmcudje2egg3cvfr.polandcentral-01.azurewebsites.net)
Short link: bit.ly/SKPH-IBD4

## [Documentation](https://tulodz-my.sharepoint.com/:w:/g/personal/247793_edu_p_lodz_pl/EWkqx71Z2zJAlRZ9zMO2aksBBXUYLX__6l3JX3fNOi1HPQ?e=hhHpki)

## Setup
1. Create `.env` file in the `docker/database` directory with the selected credentials and settings to your local database.

```conf
DB_NAME="<db_name>"
DB_USER="<user_name>"
DB_PASSWORD="<password>"
DB_PORT="<port>"
```

2. Set the `DATABASE_URI` environment variables to match the values in the `.env` file.
Set `MAIL_*` environment variables.
> **Note**: You may need to restart your terminal or IDE for the changes to take effect.
```sh
DATABASE_URI=postgresql+psycopg2://${user_name}:${password}@localhost:${port}/${db_name}
MAIL_SERVER=your-mail-server
MAIL_PORT=your-mail-port
MAIL_USE_SSL=True/False
MAIL_USE_TLS=True/False
MAIL_USERNAME=your-email-username
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=your-default-sender-email
```

3. Run the Docker Compose with the database.
```sh
docker compose -f docker/database/docker-compose.yml up -d
```

## Running the application
```sh
pybabel extract -F babel.cfg -o messages.pot . # Extracts texts from templates to translations
pybabel update -i messages.pot -d translations # Updates polish translations dictionary
pybabel compile -d translations # Compile translations
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
- Develop smaller `feature/**` branches and merge them into the `epic` branch without needing to pass CI checks or follow branch protection rules.
- When the `epic` branch is ready for integration into `main`, ensure it meets all the above requirements.
