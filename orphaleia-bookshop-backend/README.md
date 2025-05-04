# Orphaleia Book Shop Backend

This is the backend API for the Orphaleia Book Shop, a literary e-commerce platform specializing in mythology, classics, poetry, and other literary works.

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) for Python
- **Pydantic**: Data validation and settings management
- **PostgreSQL**: Relational database
- **Alembic**: Database migration tool
- **JWT**: Authentication using JSON Web Tokens

## Project Structure

```
├── alembic/              # Database migrations
├── app/                  # Application code
│   ├── api/              # API endpoints
│   │   └── v1/           # API version 1
│   │       └── endpoints/# API route handlers
│   ├── core/             # Core application code
│   ├── data/             # Sample data
│   ├── db/               # Database setup and session management
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── tests/                # Test files
├── .env.example          # Environment variables example file
├── alembic.ini           # Alembic configuration
├── requirements.txt      # Project dependencies
└── run.py                # Application entry point
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### Users

- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID (admin only)
- `PUT /api/v1/users/{user_id}` - Update user (admin only)

### Books

- `GET /api/v1/books` - List all books (with filtering)
- `POST /api/v1/books` - Create a new book (admin only)
- `GET /api/v1/books/{book_id}` - Get book by ID
- `PUT /api/v1/books/{book_id}` - Update a book (admin only)
- `DELETE /api/v1/books/{book_id}` - Delete a book (admin only)
- `GET /api/v1/books/category/{category}` - Get books by category
- `GET /api/v1/books/featured` - Get featured books

### Orders

- `GET /api/v1/orders` - List user's orders
- `POST /api/v1/orders` - Create a new order
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `PUT /api/v1/orders/{order_id}` - Update an order

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/orphaleia-bookshop.git
cd orphaleia-bookshop/orphaleia-bookshop-backend
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

## Documentation

Once the server is running, you can access the auto-generated API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with pytest:

```bash
pytest
```

## Frontend Connection

This backend is designed to connect with the [Orphaleia Book Shop Frontend](https://github.com/your-username/orphaleia-bookshop-frontend), a React application that provides the user interface.
