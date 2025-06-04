
# NCAIR API Training App (Branch: Owad)

This repository contains the **Owad** branch, which holds the active development state for the NCAIR API Training App. To work with or test this code, ensure you clone and checkout the **Owad** branch specifically.

A Python-based REST API with MySQL, migrations, CRUD operations, and Docker support.

---

## Prerequisites

* Python 3.8+ (if running locally)
* Git
* Docker & Docker Compose (to run via containers)

---

## .env Configuration

Create a file named `.env` in the project root with the following content (adjust as needed):

```ini
DB_USER=root
DB_PASSWORD=[MYSQL_DATABASE_PASS]
DB_NAME=[MYSQL_DATABASE_NAME]
DB_HOST=db [YOUR HOST]
DB_PORT=3306 [YOUR INTERNAL DB PORT ~ MYSQL DEFAULT: 3306]
```

These environment variables are used by both the application and the Docker Compose setup.

---

## Cloning the `Owad` Branch

> **Important:** Only the **Owad** branch contains the active application code. Do not clone or use other branches.

1. **Clone just the `Owad` branch**

   ```bash
   git clone --branch Owad https://github.com/kelly-ncair/ncair_advanced_training.git
   cd ncair_advanced_training
   ```

   * The `--branch Owad` flag ensures Git checks out `Owad` immediately.
   * If you have already cloned without specifying a branch, run:

     ```bash
     git fetch origin Owad
     git checkout Owad
     ```

2. **Verify you are on `Owad`**

   ```bash
   git branch --show-current
   ```

   You should see:

   ```
   Owad
   ```

---

## Running with Docker Compose (Recommended)

1. **Ensure `.env` is present**
   Confirm the `.env` file (shown above) exists in the project root.

2. **Start services**

   ```bash
   docker-compose up --build
   ```

   * **db** (MySQL) will run on port `3308` (host) → `3306` (container).
   * **math** (the API service) will build from `Dockerfile` and listen on port `3000` (container) → `4200` (host).
   * The application reads DB credentials from `.env` and connects to the `db` service.

3. **Apply database migrations**
   In a new terminal (while `docker-compose` is running), run:

   ```bash
   docker-compose exec math alembic upgrade head
   ```

   This creates the necessary tables in the `ncair` database.

4. **Access the API**
   The API is now available at:

   ```
   http://localhost:4200/
   ```

   Use Postman, curl, or any HTTP client to test endpoints defined in `routes.py` (e.g., `GET /api/v1/...`, `POST /api/v1/...`).

5. **Stop services**

   ```bash
   docker-compose down
   ```

---

## Running Locally (Optional)

> Use this if you want to run without Docker. Ensure a local MySQL server is running, and update `.env` accordingly.

1. **(If not already cloned)** Clone only the `Owad` branch:

   ```bash
   git clone --branch Owad https://github.com/kelly-ncair/ncair_advanced_training.git
   cd ncair_advanced_training
   ```

2. **Create a virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configure `.env`**
   Update the `.env` file with your local MySQL credentials (e.g., `DB_HOST=localhost`, `DB_PORT=3306`).

4. **Apply database migrations**

   ```bash
   alembic upgrade head
   ```

   This will create/update tables in your local MySQL database named `ncair`.

5. **Start the API server**

   ```bash
   python main.py
   ```

   By default, the service listens on port `3000`. You can now access it at:

   ```
   http://127.0.0.1:3000/
   ```

---

## Project Structure

```
├── alembic/                  # Alembic migration scripts
├── alembic.ini               # Alembic configuration
├── connection.py             # SQLAlchemy DB connection setup
├── crud.py                   # CRUD functions
├── Dockerfile                # Builds the API container
├── docker-compose.yml        # Defines db (MySQL) & math (API) services
├── main.py                   # Entry point (starts FastAPI/Flask server)
├── models.py                 # SQLAlchemy models
├── requirements.txt          # Python dependencies
├── routes.py                 # API route definitions
├── .env                      # Environment variables (not committed)
└── .vscode/                  # VSCode settings (optional)
```

---

## Database Migrations

* Whenever you modify `models.py`, generate a new migration:

  ```bash
  alembic revision --autogenerate -m "Your message"
  alembic upgrade head
  ```
* On Docker Compose, run migrations inside the `math` container:

  ```bash
  docker-compose exec math alembic upgrade head
  ```

---

## Notes

* The MySQL service runs with:

  * Root password: `DB_PASSWORD` from `.env`
  * Database: `ncair` (auto-created)
  * Character set: `latin1` / `latin1_swedish_ci`
  * Mapped to host port `3308` → container port `3306`.
* The API service (`math`) waits for `db` before starting, thanks to `depends_on`.
* Logs are printed to the container console by default. Tail logs with:

  ```bash
  docker-compose logs -f math
  ```

---

You’re now ready to run and test the NCAIR API Training App from the **Owad** branch. If you encounter errors, double-check that:

1. You cloned the **Owad** branch.
2. The `.env` file is correctly formatted.
3. `docker-compose up` is running without failures.
4. Migrations have been applied (`alembic upgrade head`).

*Yours Truly, Yisau Abdulwahab(AgtOwad)*