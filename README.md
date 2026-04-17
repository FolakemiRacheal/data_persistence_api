# 🚀 Data Persistence API (HNG Stage 1)

A Django REST API that integrates **Genderize, Agify, and Nationalize APIs**, processes the data, stores it, and exposes endpoints to manage profiles.

---

##  Base URL

(https://datapersistenceapi-production.up.railway.app/)

## 📡 Endpoints

* **POST** `/api/profiles` → Create profile
* **GET** `/api/profiles` → Get all profiles (supports filters)
* **GET** `/api/profiles/{id}` → Get single profile
* **DELETE** `/api/profiles/{id}` → Delete profile

---

## ⚙️ Features

* Multi-API integration
* Data processing (age group, nationality)
* No duplicate records
* Filtering support
* Proper error handling

---

## Stack

* Django
* Django REST Framework
* SQLite
* Requests

---

## Run Locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

