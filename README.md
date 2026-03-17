# ♾️ python CI/CD pipeline
![Python](https://img.shields.io/badge/python-3.11-blue) 
<a href="https://github.com/wiIliu/python-CICD-pipeline/actions"><img alt="Actions Status" src="https://github.com/wiIliu/python-CICD-pipeline/actions/workflows/tests.yml/badge.svg"></a>
[![Docker image](https://github.com/wiIliu/python-CICD-pipeline/actions/workflows/docker_build.yml/badge.svg)](https://github.com/wiIliu/python-CICD-pipeline/actions/workflows/docker_build.yml) 
![Pylint](https://github.com/wiIliu/python-CICD-pipeline/actions/workflows/pylint.yml/badge.svg) 
<a href="https://github.com/wiIliu/python-CICD-pipeline/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-purple"></a>
<!-- coverage badge to add -->
![coverage](https://img.shields.io/badge/coverage-pending-lightgrey)


Two Python microservices (Order + Analytics) that communicate via REST integrated with a PostgreSQL relational database. Each service is Dockerized, unit-tested, and has a CI pipeline that runs tests and security scans.

---

## Table of Contents

1. [Overview](#overview)  
2. [Project Structure](#project-structure)  
3. [Installation](#installation)  
   - [Setting up Environment](#setting-up-environment)  
   - [Installing Dependencies](#installing-dependencies)  
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)  
7. [References](#references)

---
<a id="overview"></a>
## 🔎 Overview

This repository contains two containerized RESTful backend microservices—an Orders Service and an Analytics Service—built using FastAPI and Docker with PostgreSQL integration.
The project also includes a CI/CD pipeline implemented with GitHub Actions that automatically runs tests, builds Docker images, and performs security analysis.

Project Components:
- Orders Microservice
- Analytics Microservice
- PostgreSQL Database
- Alembic Migrations
- Multi-stage Docker Builds
- Docker Compose Orchestration
- GitHub Actions for CI

The **Orders Microservice** implements a basic RESTful API (FastAPI) that performs CRUD operations against an `orders` database. (_Future work will include adding user authentication for additional security_)

The **Analytics Microservice** will communicate via API calls with the orders service to retrieve order data and provide calculated statistical metrics. Some of these metrics include total orders, revenue statistics, average order value, and order distribution (_Future work will include creating a basic GUI to display these results in an interactive environment_)

The services and database are coordinated using Docker Compose, allowing the entire system to be started with a single command.

### CI Pipeline
The repository includes a CI pipeline built using **GitHub Actions** that run automatically to enforce validation, Docker image builds, and code quality.

The pipeline performs the following:
- Tests - runs unit and integration tests using Pytest on every push and PR.
- Pylint - Lints the code using Pylint on every push and PR.
- Docker Build - Builds and uploads the PROD docker image to DockerHub on every PR to `main`
- CodeQL - Uses built-in GitHub CodeQL for static security analysis

### Tech Stack
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL
- Docker
- GitHub Actions
- Pytest

### Learning Goals 
This project was constructed in order to gain hands-on experience with building a CI/CD pipeline from the ground-up. It was used as a method to gain experience in connecting microservices together to build scalable architecture. 

#### ✍️ Author

LinkedIn: [Willow Connelly](https://www.linkedin.com/in/willow-connelly-28b197263/)<br>
GitHub: [WiIliu](https://github.com/wiIliu)

---
<a id="project-structure"></a>
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
<a id="installation"></a>
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
   pip install -r requirements-dev.txt
   ```

*(Make sure you are in the new python environment so that packages are installed there.)*

**Typical Requirements** (already in `requirements.txt`):
- Python 3.11 (or similar)
- FastAPI 0.128
- SQLAlchemy 2.0
- Pydantic 2.12
- Alembic 1.18

---
<a id="usage"></a>
## 🚀 Usage

#### Run services using Docker
In project root run:
```sh
docker compose up --build
```
This starts:
- Orders Service
- Analytics Service
- PostgreSQL database

> If developing locally, a `test` profile can be used to run the test containers.

Once running, each Service can be accessed locally via the generated links:

Order API: http://localhost:8000 <br>
Analytics API: http://localhost:8001

Interactive Swagger API docs:

Order API Docs: http://localhost:8000/docs<br>
Analytics API Docs: http://localhost:8001/docs

---
<a id="contributing"></a>
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
<a id="license"></a>
## 📜 License

This project is licensed under the [MIT License](LICENSE). You’re free to use, modify, and distribute the code as allowed by that license.

---
<a id="references"></a>
## 📋 References


---

_Thank you for visiting **python-CICD-pipeline**! If you have any questions or issues, feel free to open an [issue](../../issues) or reach out._


---
