# Order and Inventory Service

Backend Service without any ORM, with Raw SQL, PostgreSQL, Redis, FastAPI.

## Technologies

**FastAPI · PostgreSQL · Redis · JWT · Docker**

---

## Architecture

### 1. Concurrency Control

### 2. Idempotent Order Creation

### 3. Cache-Aside Strategy (Redis)

### 4. Raw SQL & Async Transactions

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/coderdiyorjon/mini-marketplace.git
cd mini-marketplace
```

### 2. Start Docker

```bash
docker-compose up -d
```

### 3. Create virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload --port 8080
```

### 5. Explore APIs

Open in your browser:

```text
http://localhost:8080/docs
```
