# Senator Holmes

A data-driven political analysis tool that evaluates U.S. senators based on their voting behavior, policy positions, and campaign promises.

---

## Overview

**Senator Holmes** is a full-stack application that aggregates political data and generates structured insights into how closely elected officials align with their stated positions.

The system combines:
- External APIs (e.g. Congress data)
- Custom scoring logic
- Structured data models (via Pydantic)
- Optional machine learning extensions

The goal is to provide **transparent, quantitative evaluations of political consistency and alignment**.

---

## Features

- **Senator Scoring System**
  - Computes an overall score based on multiple policy categories
  - Aggregates category-level scores into a unified metric

- **Policy Category Breakdown**
  - Each senator is evaluated across multiple dimensions:
    - Economy
    - Healthcare
    - Immigration
    - Energy
    - etc.

- **API for Data Access**
  - Query senators by state
  - Retrieve structured JSON responses

- **Extensible Data Pipeline**
  - Designed for integration with:
    - Voting records
    - Campaign promises
    - External datasets

---

## Tech Stack

- **Backend:** FastAPI  
- **Language:** Python  
- **Data Modeling:** Pydantic  
- **Data Sources:** Congress API, custom datasets  
- **Frontend (optional):** Static HTML / JS or framework-based UI  

---

## Project Structure
server/<br />
├── main.py # FastAPI app entrypoint <br />
├── src/ <br />
│ ├── database/ # Data access + senator logic <br />
│ ├── analysis/ # Scoring + processing <br /> 
│ └── models/ # Pydantic schemas <br />
client/ <br />
├── index.html # Frontend UI <br />


---

## ⚡ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/ObfuscatedFuture/Senator-Holmes.git
cd Senator-Holmes
```
### 2. Setup environment
```
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt

```

### 3. Start the server

```
uvicorn main:app --reload
```


