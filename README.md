# FlowFinance

## Overview

FlowFinance is a modern financial management application that helps users track their expenses, manage budgets, and visualize their financial data. The application consists of a React-based frontend and a robust backend system, providing a seamless experience for personal finance management.

## Project Structure

```
FlowFinance/
├── Frontend/         # React-based frontend application
├── Backend/          # FastAPI-based backend server
├── LICENSE          # MIT License
└── README.md        # This file
```

## Features

- 💰 Expense tracking and categorization
- 📊 Financial data visualization
- 📱 Responsive design for all devices
- 🔒 Secure user authentication
- 📈 Budget planning and monitoring
- 📱 Cross-platform compatibility
- 🔄 Real-time data synchronization
- 📤 Import/Export functionality

## Tech Stack

### Frontend
- React with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- shadcn-ui for UI components

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- JWT Authentication
- Alembic (Database migrations)
- Pydantic (Data validation)
- Uvicorn (ASGI server)

## Getting Started

### Prerequisites

- Node.js (LTS version)
- npm or bun package manager
- Python 3.8+
- PostgreSQL database
- Poetry (recommended) or pip

### Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/FlowFinance.git
cd FlowFinance
```

2. Set up the Frontend:
```sh
cd Frontend
npm install
# or if using bun
bun install
```

3. Set up the Backend:
```sh
cd Backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file with your database configuration
# DATABASE_URL="postgresql://user:password@host:port/database_name"
# SECRET_KEY="your-super-secret-jwt-key"
# ALGORITHM="HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES=30

# Run database migrations
alembic upgrade head
```

4. Start the development servers:

Frontend:
```sh
cd Frontend
npm run dev
# or if using bun
bun dev
```

Backend:
```sh
cd Backend
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The frontend will be available at `http://localhost:5173` and the backend API at `http://localhost:8000`.

## Development

### Frontend Development
See the [Frontend README](./Frontend/README.md) for detailed frontend development instructions.

### Backend Development
The backend provides a RESTful API with the following main endpoints:

- **Authentication**
  - `POST /register`: Register new user
  - `POST /token`: User login

- **Users**
  - `GET /users/me`: Get current user
  - `PUT /users/me`: Update user details

- **Accounts**
  - `POST /accounts`: Create account
  - `GET /accounts`: List accounts
  - `GET /accounts/{id}`: Get account details
  - `PUT /accounts/{id}`: Update account
  - `DELETE /accounts/{id}`: Delete account

- **Categories**
  - `POST /categories`: Create category
  - `GET /categories`: List categories
  - `GET /categories/{id}`: Get category details
  - `PUT /categories/{id}`: Update category
  - `DELETE /categories/{id}`: Delete category

- **Transactions**
  - `POST /transactions`: Create transaction
  - `GET /transactions`: List transactions
  - `GET /transactions/{id}`: Get transaction details
  - `PUT /transactions/{id}`: Update transaction
  - `DELETE /transactions/{id}`: Delete transaction
  - `POST /transactions/import`: Import transactions
  - `GET /transactions/export`: Export transactions

For detailed API documentation, visit `http://localhost:8000/docs` when the backend server is running.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Yuri Fabio Sanches - [Your contact information]

Project Link: [https://github.com/yourusername/FlowFinance](https://github.com/yourusername/FlowFinance)