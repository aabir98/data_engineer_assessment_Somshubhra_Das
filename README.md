# Data Engineering Assessment

Welcome!  
This exercise evaluates your core **data-engineering** skills:

| Competency | Focus                                                         |
| ---------- | ------------------------------------------------------------- |
| SQL        | relational modelling, normalisation, DDL/DML scripting        |
| Python ETL | data ingestion, cleaning, transformation, & loading (ELT/ETL) |

---

## 0 Prerequisites & Setup

> **Allowed technologies**

- **Python ≥ 3.8** – all ETL / data-processing code
- **MySQL 8** – the target relational database
- **Pydantic** – For data validation
- List every dependency in **`requirements.txt`** and justify selection of libraries in the submission notes.

---

## 1 Clone the skeleton repo

```
git clone https://github.com/100x-Home-LLC/data_engineer_assessment.git
```

✏️ Note: Rename the repo after cloning and add your full name.

**Start the MySQL database in Docker:**

```
docker-compose -f docker-compose.initial.yml up --build -d
```

- Database is available on `localhost:3306`
- Credentials/configuration are in the Docker Compose file
- **Do not change** database name or credentials

For MySQL Docker image reference:
[MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

### Problem

- You are provided with a raw JSON file containing property records is located in data/
- Each row relates to a property. Each row mixes many unrelated attributes (property details, HOA data, rehab estimates, valuations, etc.).
- There are multiple Columns related to this property.
- The database is not normalized and lacks relational structure.
- Use the supplied Field Config.xlsx (in data/) to understand business semantics.

### Task

- **Normalize the data:**

  - Develop a Python ETL script to read, clean, transform, and load data into your normalized MySQL tables.
  - Refer the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

- **Deliverable:**
  - Write necessary python and sql scripts
  - Place your scripts in `src/`
  - The scripts should take the initial json to your final, normalized schema when executed
  - Clearly document how to run your script, dependencies, and how it integrates with your database.

---

## Submission Guidelines

- Edit the section to the bottom of this README with your solutions and instructions for each section at the bottom.
- Ensure all steps are fully **reproducible** using your documentation
- DO NOT MAKE THE REPOSITORY PUBLIC. ANY CANDIDATE WHO DOES IT WILL BE AUTO REJECTED.
- Create a new private repo and invite the reviewer https://github.com/mantreshjain and https://github.com/siddhuorama

---

**Good luck! We look forward to your submission.**

## Solutions and Instructions (Filed by Candidate)
1. Start Docker

Ensure Docker Desktop is running, then start the MySQL service:

docker compose -f docker-compose.initial.yml up --build -d

2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

3️. Install dependencies
pip install -r requirements.txt

requirements.txt is a file in the root containing

mysql-connector-python
pandas
openpyxl
python-dotenv
python-dateutil
pydantic

4. Verify MySQL connection
python src\test_db.py

5. Create the database schema
python src\generate_schema_sql.py

This script creates normalized tables:

property

leads

valuation

hoa

rehab

taxes

SQL DDL is also saved as schema.sql for documentation.

6️. Run the ETL pipeline
python src\etl.py

Expected output:

connected to MySQL DB
reading data from data\fake_property_data_new.json
found N property records
etl complete


This loads all property data into the normalized MySQL schema.

7. Verify loaded data
docker exec -it mysql_ctn mysql -udb_user -p6equj5_db_user home_db -e "SHOW TABLES;"
docker exec -it mysql_ctn mysql -udb_user -p6equj5_db_user home_db -e "SELECT COUNT(*) FROM property;"
docker exec -it mysql_ctn mysql -udb_user -p6equj5_db_user home_db -e "SELECT * FROM valuation LIMIT 5;"

**Document your solution here:**
property (1) ───< leads
        │
        ├──< valuation
        ├──< hoa
        ├──< rehab
        └──< taxes
Each property can have multiple leads, valuations, rehab estimates, taxes, or HOA entries.

                             property
  ┌─────────────────────────────────────────────────────────────────┐
  │ PK property_id                                                   │
  │    property_title, address, city, state, zip, tax_rate, ...      │
  └─────────────────────────────────────────────────────────────────┘
                │1
                │
                ▼
  ┌──────────────────┬──────────────────┬──────────────┬──────────────┬──────────────┐
  │      leads       │    valuation     │     hoa      │     rehab     │    taxes     │
  │──────────────────│──────────────────│──────────────│───────────────│──────────────│
  │ PK lead_id       │ PK valuation_id  │ PK hoa_id    │ PK rehab_id   │ PK tax_id    │
  │ FK property_id ◂─┤ FK property_id ◂─┤ FK property_id◂┤ FK property_id◂┤ FK property_id◂┤
  │ reviewed_status  │ list_price       │ hoa          │ underwriting_  │ taxes        │
  │ ...              │ previous_rent    │ hoa_flag     │ rehab, flags   │              │
  └──────────────────┴──────────────────┴──────────────┴───────────────┴──────────────┘

Cardinality: property (1) ───< child_table (many)   (i.e., 1 -> N)
