# Order and Inventory Service

Backend Service without any ORM, with Raw SQL, PostgreSQL, Redis, FastAPI.


**TECHNOLOGIES** --> FastAPI, PostgreSQL, Redis, JWT, Docker

---

## Architecture

### 1. Concurrency Control
### 2. Idempotent Order Creation
### 3. Cache-Aside Strategy (Redis)
### 4. Raw SQL & Async Transactions


## Running the Project

**1. Clone repo and navigate to the project dir:**

git clone <your-repository-url>
cd mini-marketplace


**2. docker-compose up -d **

**3. python -m venv venv
vanv\Scripts\activate
pip install -r requirements.txt**

**4. uvicorn app.main:app --reload --port 8080 **

**5. Explore APIs **

Open
```http://localhost:8080/docs```
in your browser