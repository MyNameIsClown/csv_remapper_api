# 📦 csv-remapper-api

**csv-remapper-api** is the backend RESTful API built with [FastAPI](https://fastapi.tiangolo.com/) for the [`csv-remapper-lib`](https://github.com/MyNameIsClown/csv_remapper_lib) Python library.  
It provides endpoints for remapping, transforming, and processing CSV files in a structured and scalable way.

This project is part of the **CSV Remapper ecosystem**, which includes:

- [`csv_remapper_lib`](https://github.com/MyNameIsClown/csv_remapper_lib) → Core Python library for CSV transformations.
- [`csv_remapper_api`](https://github.com/MyNameIsClown/csv_remapper_api)  → REST API for remote usage and integration with web apps or other services.
- [`csv_remapper_web`](https://github.com/MyNameIsClown/csv_remapper_web)  → WEB client for make easier the use of csv tool functionalities.

---

## ✨ Features

- 🚀 **FastAPI-powered** RESTful API  
- 🔗 **Integration** with `csv-remapper-lib` for CSV parsing and transformations  
- 🧩 **Modular & testable** design for easy extension  
- 📦 **Poetry-based** dependency management  
- 🐍 **Python 3.12+** support  

---

## 📂 Project Structure

```bash
csv-remapper-api/
├── app/                    # Main API application
│   ├── api/                    
│   │   └── v1/                 
│   │       └── endpoints.py
│   │       └── router.py  
│   │       └── schemas.py 
│   │       └── utils.py   
│   └── main.py             # FastAPI entrypoint
│   └── jobs.py             # Definition of cron jobs methods
│   └── config.py           # Basic config for app
│   └── logging_config.py   # Configuration for logging
│   └── router.py           # Main app router
│   └── scheduler_config.py # Scheduler config for cron jobs
├── tests/                  # Unit and integration tests
├── files/                  # temporal folder for storing csv files
├── pyproject.toml          # Poetry dependencies and metadata
├── README.md               # This file
└── LICENSE                 # License file
```
## 🚀 Getting Started
### 1. Clone the repository

```bash
git clone https://github.com/MyNameIsClown/csv-remapper-api.git
cd csv-remapper-api
```

### 2. Install dependencies
You can use either Poetry or pip.

#### a) With Poetry (recommended)
```bash
# Install Poetry if not already installed
pip install poetry

# Install dependencies
poetry install
```

#### b) With pip
```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the API
#### With Poetry
```bash
poetry run fastapi dev
```

#### With uvicorn directly
```bash
uvicorn app.main:app --reload
```

The API will be available at:
👉 http://localhost:8000

👉 Interactive API docs: http://localhost:8000/docs

👉 Alternative docs: http://localhost:8000/redoc

## 🧪 Running Tests
```bash
poetry run pytest
```

## 🤝 Contributing
Contributions are welcome! To contribute:

1. Fork this repository

2. Create a new branch (git checkout -b feature/my-feature)

3. Commit your changes (git commit -m "Add my feature")

4. Push to your fork (git push origin feature/my-feature)

5. Open a Pull Request

Make sure to follow the existing code style and add tests when possible.

## 📜 License
This project is licensed under the AGPL License – see the [LICENSE](https://github.com/MyNameIsClown/csv_remapper_api/blob/master/LICENSE) file for details.

## 👥 Maintainers & Collaboration
- Victor Carrasco (@MyNameIsClown) – creator and maintainer
If you’d like to collaborate, feel free to reach out or open an issue. 🚀