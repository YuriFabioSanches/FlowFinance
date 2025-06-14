# Flow Finance Backend

## Project Description

This is the backend component of the Flow Finance application, built with FastAPI. It provides a robust and secure API for managing personal finance data, including user authentication, accounts, categories, and transactions. The backend is designed to be consumed by a separate frontend application.

## Features

*   **User Management**: Register, login, and manage user profiles.
*   **Authentication & Authorization**: Secure access to protected routes using JWT tokens.
*   **Account Management**: Create, read, update, and delete financial accounts.
*   **Category Management**: Organize transactions with custom categories.
*   **Transaction Management**: Record, view, and manage financial transactions.
*   **Database Integration**: Utilizes SQLAlchemy for ORM with a PostgreSQL database (configured via `.env`).

## Technologies Used

*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Uvicorn**: An ASGI server for running FastAPI applications.
*   **SQLAlchemy**: The Python SQL Toolkit and Object Relational Mapper.
*   **Psycopg2**: PostgreSQL adapter for Python.
*   **Python-Jose[cryptography]**: For JWT (JSON Web Token) handling.
*   **Passlib**: Secure password hashing library.
*   **Pydantic**: Data validation and settings management using Python type hints.
*   **Pydantic-Settings**: Pydantic's settings management with environment variables.
*   **Python-Dotenv**: Reads key-value pairs from a `.env` file and sets them as environment variables.
*   **Alembic**: Lightweight database migration tool for SQLAlchemy.
*   **Bcrypt**: Hashing algorithm for passwords.
*   **Email-Validator**: Email address validation.

## Setup Instructions

Follow these steps to set up and run the Flow Finance Backend locally.

### Prerequisites

*   Python 3.8+ (recommended)
*   Poetry (recommended for dependency management) or pip
*   PostgreSQL database instance

### 1. Clone the repository

```bash
git clone https://github.com/your-username/FlowFinance.git
cd FlowFinance/Backend
```

### 2. Set up the Virtual Environment and Install Dependencies

#### Using Poetry (Recommended)

If you have Poetry installed, simply run:

```bash
poetry install
poetry shell
```

#### Using pip

```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate # On macOS/Linux

pip install -r requirements.txt
```

### 3. Database Configuration

Create a `.env` file in the `Backend/` directory (the same level as `src` and `requirements.txt`) with your PostgreSQL database connection string and JWT secret key. Replace the placeholder values with your actual database credentials.

```env
DATABASE_URL="postgresql://user:password@host:port/database_name"
SECRET_KEY="your-super-secret-jwt-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run Database Migrations

To create the necessary database tables, run Alembic migrations. Make sure your virtual environment is activated.

```bash
alembic upgrade head
```

### 5. Run the Application

Start the FastAPI application using Uvicorn. Make sure your virtual environment is activated.

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag will automatically restart the server on code changes, which is useful for development. The API will be accessible at `http://localhost:8000`.

## API Endpoints

Below is a brief overview of the main API endpoints. For detailed request/response schemas, refer to the automatically generated OpenAPI documentation.

*   **Authentication**
    *   `POST /register`: Register a new user.
    *   `POST /token`: Obtain an access token for authentication.

*   **Users**
    *   `GET /users/me`: Get current user details.
    *   `PUT /users/me`: Update current user details.

*   **Accounts**
    *   `POST /accounts/`: Create a new account.
    *   `GET /accounts/`: List all accounts for the current user.
    *   `GET /accounts/{account_id}`: Get a specific account by ID.
    *   `PUT /accounts/{account_id}`: Update an account.
    *   `DELETE /accounts/{account_id}`: Delete an account.

*   **Categories**
    *   `POST /categories/`: Create a new category.
    *   `GET /categories/`: List all categories for the current user.
    *   `GET /categories/{category_id}`: Get a specific category by ID.
    *   `PUT /categories/{category_id}`: Update a category.
    *   `DELETE /categories/{category_id}`: Delete a category.

*   **Transactions**
    *   `POST /transactions/`: Create a new transaction.
    *   `GET /transactions/`: List all transactions for the current user.
    *   `GET /transactions/{transaction_id}`: Get a specific transaction by ID.
    *   `PUT /transactions/{transaction_id}`: Update a transaction.
    *   `DELETE /transactions/{transaction_id}`: Delete a transaction.
    *   `POST /transactions/import`: Import transactions from a file.
    *   `GET /transactions/export`: Export transactions to a file.

## API Request/Response Schemas

### Authentication

#### Register User
```json
POST /register
Request:
{
    "email": "user@example.com",
    "username": "username",
    "password": "password123"
}

Response:
{
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "is_active": true
}
```

#### Login
```json
POST /token
Request (form-data):
{
    "username": "username",
    "password": "password123"
}

Response:
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Users

#### Get Current User
```json
GET /users/me
Response:
{
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "is_active": true
}
```

#### Update Current User
```json
PUT /users/me
Request:
{
    "email": "newemail@example.com",  // optional
    "username": "newusername",        // optional
    "password": "newpassword123"      // optional
}

Response:
{
    "id": 1,
    "email": "newemail@example.com",
    "username": "newusername",
    "is_active": true
}
```

### Accounts

#### Create Account
```json
POST /accounts
Request:
{
    "name": "Checking Account",
    "initial_balance": 1000.00
}

Response:
{
    "id": 1,
    "name": "Checking Account",
    "initial_balance": 1000.00,
    "user_id": 1
}
```

#### List Accounts
```json
GET /accounts
Response:
[
    {
        "id": 1,
        "name": "Checking Account",
        "initial_balance": 1000.00,
        "user_id": 1
    },
    {
        "id": 2,
        "name": "Savings Account",
        "initial_balance": 5000.00,
        "user_id": 1
    }
]
```

#### Update Account
```json
PUT /accounts/{account_id}
Request:
{
    "name": "Updated Account Name",     // optional
    "initial_balance": 2000.00         // optional
}

Response:
{
    "id": 1,
    "name": "Updated Account Name",
    "initial_balance": 2000.00,
    "user_id": 1
}
```

### Categories

#### Create Category
```json
POST /categories
Request:
{
    "name": "Groceries"
}

Response:
{
    "id": 1,
    "name": "Groceries",
    "user_id": 1
}
```

#### List Categories
```json
GET /categories
Response:
[
    {
        "id": 1,
        "name": "Groceries",
        "user_id": 1
    },
    {
        "id": 2,
        "name": "Utilities",
        "user_id": 1
    }
]
```

#### Update Category
```json
PUT /categories/{category_id}
Request:
{
    "name": "Updated Category Name"  // optional
}

Response:
{
    "id": 1,
    "name": "Updated Category Name",
    "user_id": 1
}
```

### Transactions

#### Create Transaction
```json
POST /transactions
Request:
{
    "amount": 50.00,
    "transaction_type": "expense",  // or "revenue"
    "description": "Grocery shopping",
    "source": "Supermarket",
    "category_id": 1,              // optional
    "account_id": 1,               // optional
    "date": "2024-03-20"
}

Response:
{
    "id": 1,
    "amount": 50.00,
    "transaction_type": "expense",
    "description": "Grocery shopping",
    "source": "Supermarket",
    "category_id": 1,
    "account_id": 1,
    "date": "2024-03-20",
    "user_id": 1
}
```

#### List Transactions
```json
GET /transactions
Response:
[
    {
        "id": 1,
        "amount": 50.00,
        "transaction_type": "expense",
        "description": "Grocery shopping",
        "source": "Supermarket",
        "category_id": 1,
        "account_id": 1,
        "date": "2024-03-20",
        "user_id": 1
    },
    {
        "id": 2,
        "amount": 1000.00,
        "transaction_type": "revenue",
        "description": "Salary",
        "source": "Employer",
        "category_id": 2,
        "account_id": 1,
        "date": "2024-03-15",
        "user_id": 1
    }
]
```

#### Update Transaction
```json
PUT /transactions/{transaction_id}
Request:
{
    "amount": 75.00,                // optional
    "transaction_type": "expense",  // optional
    "description": "Updated description",  // optional
    "source": "Updated source",     // optional
    "category_id": 2,              // optional
    "account_id": 2,               // optional
    "date": "2024-03-21"          // optional
}

Response:
{
    "id": 1,
    "amount": 75.00,
    "transaction_type": "expense",
    "description": "Updated description",
    "source": "Updated source",
    "category_id": 2,
    "account_id": 2,
    "date": "2024-03-21",
    "user_id": 1
}
```

#### Import Transactions
```json
POST /transactions/import
Request:
Content-Type: multipart/form-data
file: <file>

Response:
[
    {
        "id": 1,
        "amount": 50.00,
        "transaction_type": "expense",
        "description": "Imported transaction 1",
        "source": "Source 1",
        "category_id": 1,
        "account_id": 1,
        "date": "2024-03-20",
        "user_id": 1
    },
    // ... more imported transactions
]
```

#### Export Transactions
```json
GET /transactions/export
Response:
Content-Type: application/zip
Content-Disposition: attachment; filename="transactions.zip"
```

### Error Responses

All endpoints may return the following error responses:

```json
// 400 Bad Request
{
    "detail": "Error message describing the issue"
}

// 401 Unauthorized
{
    "detail": "Could not validate credentials",
    "headers": {
        "WWW-Authenticate": "Bearer"
    }
}

// 404 Not Found
{
    "detail": "Resource not found"
}

// 500 Internal Server Error
{
    "detail": "An unexpected error occurred"
}
```

## CORS Configuration

The backend is configured with CORS (Cross-Origin Resource Sharing) middleware to allow requests from the following origins:

*   `http://localhost`
*   `http://localhost:8000`
*   `null` (for direct file access of `index.html`)
*   `http://127.0.0.1:5500` (common for VS Code Live Server)

If your frontend is served from a different origin, you will need to add that URL to the `origins` list in `Backend/src/main.py`. 
- ReDoc documentation: http://localhost:8000/redoc 