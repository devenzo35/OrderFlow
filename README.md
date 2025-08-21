# OrderFlow API

## Introduction

OrderFlow is a robust and scalable RESTful API designed to serve as the backbone for an order management system. Built with Python and FastAPI, it provides a comprehensive set of endpoints for managing users, categories, and movements. The project emphasizes clean code, modern development practices, and a secure authentication system. This API is ideal for applications requiring a reliable and efficient backend for handling order-related data.

## Features

*   **User Management:** Complete user lifecycle management, including creation, retrieval, updating, and deletion of user accounts.
*   **Secure Authentication:** JWT-based authentication to protect API endpoints and ensure secure data access.
*   **Category Management:** Functionality to create, retrieve, update, and delete categories, allowing for flexible data organization.
*   **Movement Tracking:** Endpoints for recording and managing movements, which can represent financial transactions, inventory changes, or other order-related events.
*   **Reporting:** Generation of reports in various formats, including PDF and Excel, for data analysis and business intelligence.
*   **Database Migrations:** Alembic integration for systematic and version-controlled database schema management.
*   **Containerized Environment:** Docker and Docker Compose for easy setup, deployment, and consistent development environments.

## Technologies Used

*   **Backend:** Python, FastAPI
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy
*   **Migrations:** Alembic
*   **Authentication:** JWT (JSON Web Tokens), Passlib for hashing
*   **Testing:** Pytest
*   **Containerization:** Docker, Docker Compose
*   **Reporting:** ReportLab (PDF), Openpyxl (Excel)

## API Endpoints

The API is versioned under `/api/v1` and includes the following resources:

*   `/api/v1/users`: Manage user accounts.
*   `/api/v1/auth`: Handle user authentication and token generation.
*   `/api/v1/categories`: Manage categories.
*   `/api/v1/movements`: Manage movements.
*   `/api/v1/reports`: Generate and export reports.

## Setup and Installation

To get the OrderFlow API running on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd OrderFlow
    ```

2.  **Set up environment variables:**
    Create a `.env` file in the project root and populate it with the necessary environment variables for the database connection (see `docker-compose.yml`).

3.  **Start the database:**
    ```bash
    docker-compose up -d db
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application:**
    ```bash
    fastapi dev app/main.py
    ```

## Database Migrations

Database schema changes are managed with Alembic. To apply migrations, run the following command:

```bash
alembic upgrade head
```

To create a new migration file after making changes to the SQLAlchemy models, use:

```bash
alembic revision --autogenerate -m "Your migration message"
```