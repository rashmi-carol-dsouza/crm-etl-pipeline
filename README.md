### CRM ETL Pipeline - README

# CRM ETL Pipeline

## Summary
This repository contains a data ETL pipeline for extracting and processing Freshsales CRM data using the [Freshsales API](https://developers.freshworks.com/crm/api/#introduction).
The pipeline is designed to perform data extraction, transformation, and aggregation to facilitate data analysis and reporting.

## Project Structure

The repository is aimed to make the development workflow efficient with:

1. Containerization - Locally running containerized Pipeline and Postgres DB coordinated by Docker Compose (see ./docker-compose.yml)
2. Automated Migration - Flyway (also containerized) for DB setup migrations (see db/migrations)
3. Automations - Makefile containing all the scripts a dev may need to execute aiming to minimise toil as much as possible (see ./Makefile)
4. Configurability (see ./.env)

```
.
├── crm-etl-pipeline/
│   ├── .env
│   ├── .gitignore
│   ├── data/
│   ├──scripts/ 
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── experiment-scripts/
│   ├── Makefile
│   ├── pipeline-scripts/
│   │   ├── main.py
│   │   ├── extract_data.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   ├── kpis.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── README.md
│   ├── run_etl.sh
│   ├── tables-creation/
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- Docker (optional, for containerized execution)
- [Make](https://www.gnu.org/software/make/)

### Installation

1. Clone the repository:

```sh
git clone https://github.com/your-username/crm-etl-pipeline.git
cd crm-etl-pipeline
```

2. First time setup

```sh
make setup
```

#### Environment Variables
Create a `.env` file in the root directory with the following:

```
FRESHSALES_API_KEY=<your_freshsales_api_key>
SALES_BUNDLE_ALIAS=<your_freshworks_bundle_alias>
ALL_CONTACTS_VIEW_ID=<your_contacts_view_id>
ALL_ACCOUNTS_VIEW_ID=<your_accounts_view_id>
ALL_DEALS_VIEW_ID=<your_deals_view_id>
POSTGRES_USER=your_postgres_user_here
POSTGRES_PASSWORD=your_postgres_password_here
POSTGRES_DB=your_postgres_db_here
OUTPUT_DIR=../data
```

Replace the placeholders with your actual credentials and paths.

3. Replace the placeholders in the generated .env file with your details

## Development Workflow

The development workflow involves the following steps:

1. **Setup**: Initialize the environment by installing dependencies and copying the example environment file.
    ```sh
    make setup
    ```

2. **Install**: Create a virtual environment and install the required Python packages using Poetry.
    ```sh
    make install
    ```

3. **Up**: Start the Docker containers in detached mode.
    ```sh
    make up
    ```

4. **Rebuild**: Restart the docker container + re-execute the pipeline
    ```sh
    make rebuild
    ```

5. **Down**: Stop and remove the Docker containers.
    ```sh
    make down
    ```

#### Setting Up a Cron Job
To automate running the ETL pipeline daily:

1. Open the crontab editor by running:

   ```
   crontab -e
   ```

2. Add the following line to schedule the ETL pipeline to run every day at midnight:

   ```
   0 0 * * * docker run -v $(pwd)/data:/app/data --env-file /path/to/.env crm_etl_pipeline
   ```

   Replace `/path/to/.env` with the actual path to your `.env` file.

#### Troubleshooting
- Make sure Docker is installed and running before running the Docker commands.
- Verify the `.env` file contains correct API keys and view IDs.
- Ensure your PostgreSQL server is set up and running properly.

## Documentation

For more detailed information see docs/