# Shareholder Management System

## Project Overview

Shareholder Management System is a web application built using Python Flask, Pandas, MySQL, HTML, CSS, Bootstrap and JavaScript.

The application allows users to:

* Upload Excel files
* Import Excel data into MySQL
* View shareholder records
* Search shareholder data
* View dashboard statistics
* Download reports

---

## Tech Stack

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* DataTables

### Backend

* Python
* Flask
* Pandas

### Database

* MySQL

---

## Project Structure

```text
Shareholder_Project/

│ app.py
│ README.md
│ .gitignore

├── templates/
│    dashboard.html

├── static/
│   ├── css/
│   │    style.css
│   │
│   └── js/
│        script.js

├── uploads/

└── venv/
```

---

## Features

* Upload Excel File
* Import Data into MySQL
* Dashboard Analytics
* Search Shareholders
* View Records
* Download Reports

---

## Installation

### Clone Repository

```bash
git clone https://github.com/princegupta2024/shareholder-management-system.git
```

### Move into project folder

```bash
cd shareholder-management-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install flask pandas openpyxl mysql-connector-python
```

### Run Project

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

## Database

Database Name:

```text
kinheridencecompanydb
```

Table Name:

```text
shareholder_data
```

---

## Author

Prince Gupta
