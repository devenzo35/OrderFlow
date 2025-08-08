# Project Context: OrderFlow

This document provides a comprehensive overview of the OrderFlow project, including its product vision, technical architecture, and development roadmap. Its purpose is to align all development efforts with the core goals of the product.

---

## 1. Product Vision & Definition

*This section is a summary of the full `PRODUCT_DEFINITION.md` file.*

**The vision for OrderFlow is to provide small businesses and individuals with the simplest, most intuitive platform for managing and analyzing their financial movements.**

### Core User Problems:
- Difficulty in tracking expenses, income, and investments.
- Lack of clear, actionable insights from financial data.
- Need for a simple, centralized system to manage financial records.

### Key User Stories:
- **As a user, I want to securely register and log in to manage my finances.**
- **As a user, I want to record all my financial movements (income, expenses, investments) with relevant details like date, amount, and category.**
- **As a user, I want to see a dashboard with visual reports (e.g., monthly balance, spending by category) to understand my financial health.**
- **As a user, I want to be able to export my data to standard formats like CSV or PDF for my records.**

---

## 2. Features & Development Roadmap

This outlines the planned features for the application.

### Core Features (MVP)
- [x] **User Authentication:** Secure user registration and login using JWT.
- [x] **Role-Based Access Control:** Distinction between regular Users and Administrators.
- [x] **CRUD for Movements:** Create, Read, Update, and Delete financial movements (income, expenses).
- [x] **Category Management:** Allow users to categorize their movements.
- [ ] **Reporting Dashboard:** A basic dashboard showing key metrics.
- [ ] **Data Export:** Export financial data to CSV and PDF.

### Future Enhancements
- [ ] **Advanced Reporting:** More detailed and customizable reports with filtering.
- [ ] **Investment Tracking:** Specific features for tracking investment performance.
- [ ] **External API Integration:** Connect to financial APIs for real-time data (e.g., stock prices, currency conversion).
- [ ] **Background Tasks:** Use Celery and Redis for sending email reports or notifications.
- [ ] **API Versioning:** Introduce versioning (e.g., `/api/v1/...`) for future compatibility.
- [ ] **Full Test Coverage:** Comprehensive unit, integration, and end-to-end tests.
- [ ] **CI/CD Pipeline:** Automated testing and deployment using Docker and GitHub Actions.

---

## 3. Technical Architecture

### Technology Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy with Alembic for migrations
- **Authentication:** JWT with passlib for password hashing
- **Testing:** Pytest
- **Containerization:** Docker, Docker-Compose

### Directory Structure
The project follows a standard FastAPI application structure:

```
/app
    /core       # Core logic, auth, config
    /db         # Database session and configuration
    /models     # SQLAlchemy ORM models
    /router     # API endpoint routers
    /schemas    # Pydantic schemas for data validation
    /services   # Business logic (reporting, etc.)
/tests          # Application tests
/alembic        # Database migration scripts
Dockerfile
docker-compose.yml
...
```

---

## 4. Business Rules

*A summary of key business rules. See `PRODUCT_DEFINITION.md` for the full list.*

- A user's email must be unique.
- A movement must have a date, description, amount, and category.
- A user can only manage their own movements.
- An administrator has full access to all data for management purposes.
