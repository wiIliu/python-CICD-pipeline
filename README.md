# python-CICD-pipeline
Two Python microservices (Order + Analytics) that communicate via REST integrated with a postgresql relational database. Each service is Dockerized, unit-tested, and has a CI pipeline that runs tests and security scans.

---


## Table of Contents

1. [Overview](#overview)  
2. [Project Structure](#project-structure)  
3. [Installation](#installation)  
   - [Creating & Activating a Python Environment](#creating--activating-a-python-environment)  
   - [Installing Dependencies](#installing-dependencies)  
4. [Usage](#usage)  
5. [License](#license)  
6. [References](#references)

---
## Overview

---

## Project Structure


```
.
├──── models/ # holds all .pth model exports
├──── webdemo/ # code for website demo and info
| ├── index.html
| ├── methodology.html
| ├── challenges.html
| ├── results.html
| ├── future-work.html
| ├── server.js
| ├──── static/
| | ├── app.js
| | ├── style.css
├── dataPreprocessing.py   # Script to load and split RT-IoT2022
└── requirments.txt/environment.yml          # Dependencies/Environment needed for this project
```

---

## Installation

### Creating & Activating a Python Environment

  
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

Within your **activated** conda environment:

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

*(Make sure you are in the new python environment so packages are installed there.)*

**Typical Requirements** (already in `requirements.txt`):
- Python 3.11 (or similar)
- FastAPI
- SqlAlchemy
- pytest

---

## Usage

---

## Contributing

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
4. **Open a Pull Request** into the main branch.

We welcome suggestions, bug reports, and community contributions!

---

## License

This project is licensed under the [MIT License](LICENSE). You’re free to use, modify, and distribute the code as allowed by that license.

---

## References


---

_Thank you for visiting **python-CICD-pipeline**! If you have any questions or issues, feel free to open an [issue](../../issues) or reach out._


---
