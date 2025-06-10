# NCAIR Training: RESTful API • Docker • Alembic • CRUD

**Branch:** `dayo_db/ncair_advanced_training`

This branch houses the code and configuration for the National Center for Artificial Intelligence and Robotics (NCAIR) hands-on training, focusing on building a RESTful API service with full CRUD operations, schema migrations via Alembic, and containerization with Docker.

---

## Tech Stack

- **Python 3.10+**  
- **Flask** – high-performance REST framework  
- **SQLAlchemy** – ORM for database modeling  
- **Alembic** – database migrations  
- **MySQL** – relational database  
- **Docker & Docker Compose** – containerization and orchestration  

---

## Features

- **CRUD Operations via API Access** for a sample resource (e.g., `Item`, `User`)
- **Alembic Migrations** to version and evolve the database schema
- **Dockerized Services** including API app and PostgreSQL


---

## Prerequisites

- Docker & Docker Compose installed  
- Git (to checkout this branch)  
- (Optional) Python 3.10+ & virtualenv, if running locally without Docker  

---

## Installation & Setup

1. **Clone just the `dayo_db` branch**

 ```bash
   git clone --branch dayo_db https://github.com/kelly-ncair/ncair_advanced_training.git
   cd ncair_advanced_training
   ```

2. **Verify you are on `dayo_db`**

   ```bash
   git branch --show-current
   ```

## Running with Docker Compose (Recommended)

1. **Start services**

   ```bash
   docker-compose up --build
   ```

   * **dbase** (MySQL) will run on port `4409` (host) → `3306` (container).
   * **api** (the API service) will build from `Dockerfile` and listen on port `4000` (host) → `3000` (container).


2. **Apply database migrations**
   In a new terminal (while `docker-compose` is running), run:

   ```bash
   docker-compose exec math alembic upgrade head
   ```

   This creates the necessary tables in the `ncair_db` database.

3. **Access the API**
   The API is now available at:

   ```
   http://localhost:4000/
   ```

   Use Postman, curl, or any HTTP client to test endpoints defined in `routes.py` (e.g., `GET /api/v1/...`, `POST /api/v1/...`).

4. **Stop services**

   ```bash
   docker-compose down
   ```

---