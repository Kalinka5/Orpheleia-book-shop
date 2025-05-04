# Orphaleia Book Shop

Orphaleia Book Shop is an online e-commerce platform specialized in mythology, classics, poetry, and literary works. The application consists of a React frontend and a FastAPI backend.

## Project Structure

- `/orphaleia-bookshop-frontend` - React frontend application
- `/orphaleia-bookshop-backend` - FastAPI backend application

## Frontend

The frontend is built with React, Vite, TypeScript, and Tailwind CSS. The frontend code lives in a separate GitHub repository and is included here as a subdirectory for development convenience.

**Frontend GitHub Repository**: [https://github.com/your-username/orphaleia-bookshop-frontend](https://github.com/your-username/orphaleia-bookshop-frontend)

### Frontend Technologies

- React with TypeScript
- Tailwind CSS for styling
- shadcn-ui for UI components
- React Router for navigation
- React Query for data fetching

## Backend

The backend is built with FastAPI, a modern Python web framework for building APIs. It provides RESTful endpoints for the frontend to interact with the database.

### Backend Technologies

- FastAPI - Python web framework
- SQLAlchemy - ORM for database operations
- Pydantic - Data validation and settings management
- Alembic - Database migrations
- PostgreSQL - Database

### API Features

- User authentication (JWT tokens)
- Book management (CRUD operations)
- Order processing
- User profile management

## Running the Application

### Backend Setup

1. Navigate to the backend directory:

```bash
cd orphaleia-bookshop-backend
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example` and configure your environment variables.

5. Set up the database:

```bash
alembic upgrade head
```

6. Run the development server:

```bash
python run.py
```

The API will be available at http://localhost:8000.

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd orphaleia-bookshop-frontend
```

2. Install dependencies:

```bash
npm install
```

3. Run the development server:

```bash
npm run dev
```

The frontend will be available at http://localhost:5173.

## About Orphaleia Book Shop

Orphaleia Book Shop offers a curated selection of books focusing on mythology, classics, poetry, philosophy, and other literary genres. Our mission is to provide readers with high-quality editions of timeless works that explore the rich tapestry of human stories across cultures and eras.

### Features

- Browse books by category
- Search for books
- View detailed information about each book
- User authentication and profile management
- Shopping cart functionality
- Order processing and tracking
