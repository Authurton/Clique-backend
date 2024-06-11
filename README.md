# Clique-of-10 Backend

This is the backend for the Clique-of-10 application, a group chat platform where users can join and create groups, send messages, and more. The backend is built with Django and Django REST Framework.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.x
- Django 3.x
- Django REST Framework

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/clique-of-10-backend.git
    cd clique-of-10-backend
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv or virtualenv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Running migrations:**
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

## Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=your-database-host
DB_PORT=your-database-port
