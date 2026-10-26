# SQL Server to PostgreSQL Data Pipeline

A Python-based data engineering project that extracts customer data from Microsoft SQL Server, transforms and cleans the data, and loads it into PostgreSQL. The project demonstrates core ETL/ELT pipeline concepts, database connectivity, data quality, incremental loading, and automated testing.

## Project Overview

This pipeline moves customer data from a SQL Server source database to a PostgreSQL target database.

**Pipeline flow:**

`SQL Server → Python Extraction → Data Transformation → PostgreSQL Loading → Audit & Watermark`

The project is designed to demonstrate how a local data pipeline can be built, tested, and improved using open-source Python tools and relational databases.

## Technologies Used

- **Python** — Pipeline orchestration and data processing
- **Microsoft SQL Server Express** — Source database
- **PostgreSQL** — Target database
- **pyodbc** — SQL Server connectivity
- **psycopg2** — PostgreSQL connectivity
- **pytest** — Automated testing
- **pandas** — Data validation and comparison
- **Git & GitHub** — Version control and project hosting

## Project Structure

```text
ETL_Sql_to_Postgresql_Data_pipeline/
│
├── config/
│   ├── __init__.py
│   ├── sql_server_connection.py
│   └── postgresql_connection.py
│
├── data_pipeline/
│   ├── __init__.py
│   ├── data_extraction.py
│   ├── data_transformation.py
│   ├── data_load.py
│   ├── pipeline_control.py
│   └── pipeline_audit.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_customer_data.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

*Adjust the structure above if your actual files differ.*

## How the Pipeline Works

### 1. Data Extraction

Extracts customer records from the `source_data.customers` table in SQL Server.

Source fields:

- `customer_id`
- `customer_name`
- `email`
- `country`
- `updated_at`

### 2. Data Transformation

Applies basic data-cleaning rules using Python:

- Removes leading and trailing spaces from customer names.
- Removes extra spaces and converts email addresses to lowercase.
- Standardizes country names using title case.
- Preserves customer IDs and update timestamps.

### 3. Data Loading

Loads transformed records into the `public.customers` table in PostgreSQL.

The pipeline uses an upsert strategy to insert new customers and update existing customers, provided the source record meets the configured timestamp condition.

### 4. Incremental Loading

The pipeline can use a previously saved watermark based on `updated_at` to identify records for subsequent runs.

A persisted watermark helps avoid repeatedly processing the entire source table. Correct incremental processing depends on reliable source timestamps and successful pipeline-control updates.

### 5. Pipeline Audit

The pipeline can record successful executions, including execution timestamps and record counts.

Audit records should only be written after the required pipeline steps succeed. Failed executions should be logged separately so that errors can be investigated.

### 6. Automated Testing

The project includes a testing layer using pytest and pandas to help validate:

- Source and target record counts, where a full mirror is expected.
- Duplicate customer IDs.
- Missing customer records in the target.
- Data transformation rules.
- Source-to-target data consistency.

## Prerequisites

Install the following before running the project:

- Python
- Microsoft SQL Server Express
- A compatible Microsoft SQL Server ODBC driver
- PostgreSQL
- Git

You will also need access to the source and target databases.

## Setup Instructions

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/sql-server-to-postgresql-data-pipeline.git
cd sql-server-to-postgresql-data-pipeline
```

Replace `YOUR_USERNAME` and the repository name with your actual GitHub details.

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate it in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure database connections

Configure the SQL Server and PostgreSQL connection modules to use your local database settings.

**Security note:** Never commit database passwords, access tokens, or other secrets to GitHub. Use environment variables or a local environment file excluded by `.gitignore`.

### Step 5: Prepare the databases

Ensure the source database and customer table exist in SQL Server.

Create the target customer table in PostgreSQL with matching columns and a primary key or unique constraint on `customer_id` for upsert operations.

If the project uses pipeline-control and audit tables, create those tables as well.

### Step 6: Run the pipeline

From the project root:

```bash
python main.py
```

### Step 7: Run automated tests

```bash
python -m pytest tests/ -v
```

Some tests compare the source and target databases directly, so ensure both databases are available and contain appropriate test data before running them.

## Key Data Engineering Concepts Demonstrated

- Database-to-database data integration
- Python ETL pipeline development
- Data cleaning and standardization
- Incremental data extraction
- Upsert-based loading
- Watermark management
- Pipeline execution auditing
- Source-to-target data validation
- Automated testing
- Git-based version control

## Future Enhancements

- Add structured logging and detailed failure records.
- Improve watermark handling and recovery after failed runs.
- Add retry logic and stronger transaction management.
- Implement data-quality rules for nulls, invalid emails, and duplicate records.
- Add unit tests with mocks and integration tests for the databases.
- Add Docker support for reproducible local environments.
- Explore orchestration using Apache Airflow.
- Add a cloud storage or warehouse target as a future extension.

## Author

**Md Shadab Alam**

Aspiring Data Engineer | Python | SQL | PostgreSQL | SQL Server

GitHub: https://github.com/YOUR_USERNAME

---

*This project is intended for learning and portfolio demonstration. Update this documentation to reflect the features verified in your actual code.*
