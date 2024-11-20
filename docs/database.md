# Database

## Tooling

- PostgreSQL
- [Flyway](https://flywaydb.org/documentation) - database migration tool to support versioning and automating database changes.

## Getting Started

Executing the `make run` command sets up a containerized postgres database that runs locally.
Flyway executes migrations in `db/migrations` to setup the database locally if it doesn't already exist.

## Schema

### Entities & Relationships

Freshsales CRM is used to manage customers, accounts, deals, and interactions.

- Contacts - may be customers or business owners.
- Accounts - are businesses. Each account may be associated with one or more contacts.
- Deals - are projects of a certain value that an account is involved in.

## Key Assumptions

- Email is safe and sufficient to use as a primary key for contacts.

### Tables

### Table 1: `contacts`
| Column Name                 | Data Type   | Description                                   |
|-----------------------------|-------------|-----------------------------------------------|
| `avatar`                   | TEXT        | URL or location for the contact's avatar     |
| `cf_last_contacted_date`   | DATETIME    | Last contacted date for the contact          |
| `cf_lead_source`           | VARCHAR     | Lead source information                      |
| `city`                     | VARCHAR     | City name                                    |
| `country`                  | VARCHAR     | Country name                                 |
| `created_at`               | DATETIME    | Record creation timestamp                    |
| `customer_fit`             | VARCHAR     | Fit information for customer                 |
| `display_name`             | VARCHAR     | Display name of the contact                  |
| `email`                    | VARCHAR     | Contact's email address                      |
| `first_name`               | VARCHAR     | First name of the contact                    |
| `id`                       | BIGINT (PK) | Primary Key: Unique identifier for contact   |
| `is_deleted`               | BOOLEAN     | Flag indicating if the record is deleted     |
| `job_title`                | VARCHAR     | Contact's job title                          |
| `last_assigned_at`         | DATETIME    | Timestamp when last assigned                 |
| `last_name`                | VARCHAR     | Last name of the contact                     |
| `lead_score`               | INTEGER     | Contact lead score                           |
| `linkedin`                 | VARCHAR     | LinkedIn profile link                        |
| `mcr_id`                   | VARCHAR     | MCR identifier                               |
| `mobile_number`            | VARCHAR     | Contact's mobile number                      |
| `open_deals_amount`        | DECIMAL     | Amount of open deals                         |
| `open_deals_count`         | INTEGER     | Number of open deals                         |
| `record_type_id`           | BIGINT      | Record type identifier                       |
| `sms_subscription_status`  | VARCHAR     | SMS subscription status                      |
| `state`                    | VARCHAR     | State of the contact                         |
| `subscription_status`      | VARCHAR     | Subscription status of contact               |
| `subscription_types`       | VARCHAR     | Subscription types                           |
| `time_zone`                | VARCHAR     | Contact's time zone                          |
| `updated_at`               | DATETIME    | Last updated timestamp                       |
| `won_deals_amount`         | DECIMAL     | Amount of won deals                          |
| `won_deals_count`          | INTEGER     | Count of won deals                           |

---

### Table 2: `accounts`
| Column Name               | Data Type   | Description                                   |
|---------------------------|-------------|-----------------------------------------------|
| `id`                     | BIGINT (PK) | Primary Key: Unique sales account identifier  |
| `address`                | VARCHAR     | Address of the sales account                 |
| `annual_revenue`         | DECIMAL     | Annual revenue of the sales account          |
| `appointments`           | VARCHAR     | Appointment information                      |
| `avatar`                 | TEXT        | Avatar or URL                                |
| `cf_account_value`       | DECIMAL     | Value of the account                         |
| `cf_region`              | VARCHAR     | Account region                               |
| `city`                   | VARCHAR     | City of sales account                        |
| `conversations`          | VARCHAR     | Conversation information                     |
| `country`                | VARCHAR     | Country of sales account                     |
| `created_at`             | DATETIME    | Record creation timestamp                    |
| `document_associations`  | VARCHAR     | Document associations for the account        |
| `facebook`               | VARCHAR     | Facebook link                                |
| `is_deleted`             | BOOLEAN     | Flag indicating if the record is deleted     |
| `last_assigned_at`       | DATETIME    | Timestamp of last assignment                 |
| `linkedin`               | VARCHAR     | LinkedIn link                                |
| `name`                   | VARCHAR     | Account name                                 |
| `notes`                  | TEXT        | Notes regarding the account                  |
| `number_of_employees`    | INTEGER     | Number of employees                          |
| `open_deals_amount`      | DECIMAL     | Amount of open deals                         |
| `open_deals_count`       | INTEGER     | Number of open deals                         |
| `owner_id`               | BIGINT      | Account owner identifier                     |
| `phone`                  | VARCHAR     | Phone number                                 |
| `record_type_id`         | BIGINT      | Record type identifier                       |
| `state`                  | VARCHAR     | State of sales account                       |
| `tasks`                  | TEXT        | Task information                             |
| `twitter`                | VARCHAR     | Twitter link                                 |
| `updated_at`             | DATETIME    | Last updated timestamp                       |
| `website`                | VARCHAR     | Sales account website                        |
| `won_deals_amount`       | DECIMAL     | Amount of won deals                          |
| `won_deals_count`        | INTEGER     | Count of won deals                           |
| `zipcode`                | VARCHAR     | Zipcode of the account                       |

---

### Table 3: `deals`
| Column Name                          | Data Type   | Description                                   |
|--------------------------------------|-------------|-----------------------------------------------|
| `id`                                | BIGINT (PK) | Primary Key: Unique deal identifier           |
| `age`                               | INTEGER     | Age of the deal                              |
| `amount`                            | DECIMAL     | Deal amount                                  |
| `cf_deal_size`                      | VARCHAR     | Deal size category                           |
| `cf_deal_stage`                     | VARCHAR     | Deal stage                                   |
| `cf_probability_of_closure`         | DECIMAL     | Probability of closing the deal              |
| `closed_date`                       | DATETIME    | Closed date                                  |
| `created_at`                        | DATETIME    | Record creation timestamp                    |
| `deal_pipeline_id`                  | BIGINT      | Deal pipeline identifier                     |
| `deal_prediction`                   | VARCHAR     | Prediction for deal outcome                  |
| `deal_prediction_last_updated_at`   | DATETIME    | Prediction last updated timestamp            |
| `deal_stage_id`                     | BIGINT      | Deal stage identifier                        |
| `expected_close`                    | DATETIME    | Expected close date                          |
| `expected_deal_value`               | DECIMAL     | Expected value of deal                       |
| `forecast_category`                 | VARCHAR     | Forecast category of the deal                |
| `has_products`                      | BOOLEAN     | Indicates if deal has products               |
| `last_assigned_at`                  | DATETIME    | Timestamp when last assigned                 |
| `name`                              | VARCHAR     | Deal name                                    |
| `probability`                       | DECIMAL     | Probability of winning                       |
| `record_type_id`                    | BIGINT      | Record type identifier                       |
| `updated_at`                        | DATETIME    | Last updated timestamp                       |
| `sales_account_id`                  | BIGINT (FK) | Foreign Key: References `accounts(id)`       |

---

### Table 4: `companies`
| Column Name       | Data Type   | Description                                   |
|-------------------|-------------|-----------------------------------------------|
| `contact_id`     | BIGINT (PK) | Primary Key: Unique identifier for contact   |
| `sales_account_id`| BIGINT (FK) | Foreign Key: References `accounts(id)`       |



