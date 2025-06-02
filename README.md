
---

# 🧺 Easy Drying – Laundry Service API

**Easy Drying** is a Django Rest Framework (DRF)-based backend API for an online laundry and drying service platform. It enables users to browse services, manage orders, leave reviews, and authenticate securely with JWT using Djoser. The project is organized into three core apps: `users`, `services`, and `orders`.

---

## 📚 Features

* 🔐 **JWT Authentication** with Djoser
* 🧼 **Service Management** with category and image support
* 🛒 **Cart and Order** system with detailed item tracking
* ⭐ **Review System** with rating and comments
* 📦 **Order Status Tracking** (e.g., Not Paid, Shipped, Delivered)
* 📄 **Swagger API Documentation** via `drf-yasg`

---

## 🧱 Project Structure

```
easy_drying/
├── users/       # Custom user model and profile management
├── services/    # Service, category, images, and reviews
├── orders/      # Cart, order processing, and order items
├── settings.py  # JWT setup, installed apps, media, etc.
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/easy-drying.git
cd easy-drying
```

### 2. Create and activate virtual environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

---

## 🔐 Authentication

The project uses **JWT Authentication** via [Djoser](https://djoser.readthedocs.io/).
You can register and log in users using endpoints like:

* `POST /auth/users/`
* `POST /auth/jwt/create/`
* `POST /auth/jwt/refresh/`

---

## 🗂️ API Endpoints

Explore all available API endpoints using the Swagger UI:

```
http://localhost:8000/swagger/
```
If want to use **Django** and a **virtual environment**, the best practice is to:

* Create a `.env` file in your project root.
* Use `python-dotenv` to load environment variables from `.env`.
* Access them in `settings.py` using `os.environ.get()`.

Here is the complete section you can copy-paste into your `README.md`:


## 📁 Environment Variable Setup

To keep sensitive settings secure and clean, use a `.env` file with `python-dotenv` in your Django project.

### ✅ 1. Sample `.env` File

Create a `.env` file in the root of your project and add:

````markdown
# Django secret settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (PostgreSQL)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# JWT (optional)
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=5
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=30

# Media
MEDIA_URL=/media/
MEDIA_ROOT=media/
````

> Do **NOT** commit this file to version control. Add `.env` to your `.gitignore`.

---

### ✅ 2. Install `python-dotenv` in your virtual environment

```bash
pip install python-dotenv
```

---

### ✅ 3. Load `.env` in `settings.py`

At the top of your `settings.py` file:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent
```

---

### ✅ 4. Use Environment Variables in `settings.py`

```python
# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# Media
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', 'media/')
```

---

Key endpoints include:

### 🔹 User

* Register, login, profile update
* View and manage personal info

### 🔹 Services

* `GET /services/`
* `GET /services/{id}/`
* `POST /services/` *(admin only)*
* Review, image upload, and availability check

### 🔹 Cart & Orders

* Add/remove items from cart
* Place and track orders
* Manage order status

---

## 🧩 Models Overview

### User

Custom user model with fields:

* `email`, `address`, `phone_number`, `bio`, `prof_image`

### Service & Category

* Services belong to categories
* Each service supports multiple images and reviews

### Cart & Order

* One cart per user
* Orders include multiple `OrderItem`s with quantity and pricing
* Status choices include: *Not Paid*, *Ready To Ship*, *Canceled*, *Shipped*, *Delivered*

---

## 🖼️ Media & File Uploads

Service and profile images are stored in:

* `Profile/prof_images/`
* `services/`

File size is validated using custom validators.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork the repository, open issues, or submit pull requests.

---

## 📬 Contact

For any queries or support, reach out to:

**Developer:** *Tanvir Chowdhury*
**Email:** *[contact@easy_drying.com](mailto:contact@easy_drying.com)*

---

