# ♾️ python-CICD-pipeline

Two Python microservices (Order + Analytics) that communicate via REST integrated with a postgresql relational database. Each service is Dockerized, unit-tested, and has a CI pipeline that runs tests and security scans.

### CI / Quality Status
![Python](https://img.shields.io/badge/python-3.11-blue)
![Tests](https://github.com/wiIliu/python-CICD-pipeline/actions/workflows/tests.yml/badge.svg)
![Docker Build](https://github.com/wiIliu/python-CICD-pipeline/actions/workflows/docker_build.yml/badge.svg)
![Pylint](https://github.com/wiIliu/python-CICD-pipeline/actions/workflows/pylint.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)


---


## Table of Contents

1. [Overview](#🔎-overview)  
2. [Project Structure](#🏗️-project-structure)  
3. [Installation](#⬇️-installation)  
   - [Setting up Environment](#setting-up-environment)  
   - [Installing Dependencies](#installing-dependencies)  
4. [Usage](#usage)
5. [Contributing](#🤝-contributing)
6. [License](#📜-license)  
7. [References](#📋-references)

---
## 🔎 Overview

---

## 🏗️ Project Structure


#### General project structure per service
```
.
{name}_service/ # the service folder
├──── alembic/ # holds all database migrations
├──── app/ # code for api and supporting elements
| ├─── main.py
| ├──── api/
| | ├──── v1/
| | | ├─── {service_routes}.py
| | | ├─── health.py # healthcheck routes
| ├──── core/ # configuration and database settings
| ├──── db_logic/
| | | ├─── crud.py # service table crud logic
| ├──── dependencies/
| ├──── models/
| ├──── schemas/
├──── tests/
| ├──── factories/
| ├──── integration_tests/
| ├──── unit_tests/
| | ├──── crud_tests/
| | ├──── schema_tests/
# misc
├── alembic.ini
├── Dockerfile
├── docker-entrypoint.sh
└── requirements.txt / requirements-dev.txt
```

---

## ⬇️ Installation

### Setting up Environment

1. **Create** a new environment (example name: `myproject`):  
   ```bash
   python -m venv myproject
   ```
2. **Activate** it:

   Windows
   ```bash
   myproject\Scripts\activate
   ```

   MacOS / Linux
   ```sh
   source myproject/bin/activate
   ```

### Installing Dependencies

Within your **activated** environment:

1. Update pip
   ```bash
   python -m pip install --upgrade pip
   ```

2. Install dependencies via requirements file
   
   Prod Requirements file
   ```bash
   pip install -r requirements.txt
   ```
   
   Dev Requirements file
   ```bash
   pip install -r requirements_dev.txt
   ```

*(Make sure you are in the new python environment so that packages are installed there.)*

**Typical Requirements** (already in `requirements.txt`):
- Python 3.11 (or similar)
- FastAPI 0.128
- SQLAlchemy 2.0
- Pydantic 2.12
- Alembic 1.18

---

## Usage

#### Run services using Docker
In project root run:
```sh
docker compose up --build
```

Once running, each Service can be accessed locally via the generated links.<br>
Order API: http://localhost:8000 <br>
Analytics API: http://localhost:8001

---

## 🤝 Contributing

1. **Fork** this repository.  
2. **Create** a new branch for your feature/fix:
   ```bash
   git checkout -b feature-my-improvement
   ```
3. **Commit** your changes and push to your fork:
   ```bash
   git commit -m "Add my new feature"
   git push origin feature-my-improvement
   ```
4. **Open a Pull Request** into the `dev` branch.

_NOTE:_ The `main` branch is protected and only updated through
approved pull requests from the `dev` branch.<br>

After review and testing, changes will be merged into `main` during the next release.

We welcome suggestions, bug reports, and community contributions!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). You’re free to use, modify, and distribute the code as allowed by that license.

---

## 📋 References


---

_Thank you for visiting **python-CICD-pipeline**! If you have any questions or issues, feel free to open an [issue](../../issues) or reach out._


---
