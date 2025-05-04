# Orphaleia Book Shop API Setup

This document explains how to set up and use the API connection between the frontend and backend of the Orphaleia Book Shop application.

## Overview

The communication between the frontend and backend is handled through a RESTful API using HTTP requests. The frontend uses Axios to make requests to the backend API endpoints.

## Backend Setup

1. Navigate to the backend directory:

   ```
   cd orphaleia-bookshop-backend
   ```

2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create the database tables:

   ```
   python create_tables.py
   ```

4. Start the backend server:
   ```
   uvicorn main:app --reload
   ```

The backend server will run on http://localhost:8000 by default.

## CORS Configuration

The backend is configured to accept cross-origin requests from the following origins:

- http://localhost:5173 (Vite default dev server)
- http://localhost:3000 (React/Next.js default)
- http://localhost:8080 (Alternative port)
- http://127.0.0.1:5173, http://127.0.0.1:3000, http://127.0.0.1:8080 (IP variants)
- https://orphaleia-bookshop.example.com (Example production domain)

To modify the allowed origins:

1. Edit the `.env` file in the backend directory
2. Update the `CORS_ORIGINS` value with a comma-separated list of allowed origins
3. Restart the backend server

Example:

```
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,https://your-production-domain.com
```

## Frontend Setup

1. Navigate to the frontend directory:

   ```
   cd orphaleia-bookshop-frontend
   ```

2. Install the dependencies:

   ```
   npm install
   ```

3. Create a `.env` file in the root of the frontend directory with the following content:

   ```
   VITE_API_URL=http://localhost:8000/api/v1
   ```

4. Start the frontend development server:
   ```
   npm run dev
   ```

The frontend will run on http://localhost:5173 by default.

## API Implementation

The API communication is implemented in the `src/lib/api.ts` file, which provides:

- A configured Axios instance with the base URL and authentication handling
- Organized API service modules for books, auth, orders, and users
- Type-safe response handling using TypeScript interfaces

### Using the API in Components

The API services can be imported and used in components as follows:

```typescript
import { booksApi } from "@/lib/api"
import { useEffect, useState } from "react"
import { Book } from "@/types/book"

function MyComponent() {
	const [books, setBooks] = useState<Book[]>([])
	const [isLoading, setIsLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)

	useEffect(() => {
		const fetchBooks = async () => {
			try {
				setIsLoading(true)
				const data = await booksApi.getBooks()
				setBooks(data)
			} catch (err) {
				console.error("Error fetching books:", err)
				setError("Failed to load books")
			} finally {
				setIsLoading(false)
			}
		}

		fetchBooks()
	}, [])

	// Render component...
}
```

## Available API Endpoints

### Books

- `GET /api/v1/books` - Get all books with optional filtering
- `GET /api/v1/books/{book_id}` - Get a single book by ID
- `GET /api/v1/books/featured/` - Get featured books
- `GET /api/v1/books/category/{category}` - Get books by category
- `POST /api/v1/books` - Create a new book (admin only)
- `PUT /api/v1/books/{book_id}` - Update a book (admin only)
- `DELETE /api/v1/books/{book_id}` - Delete a book (admin only)

### Authentication

- `POST /api/v1/auth/login` - Log in a user
- `POST /api/v1/auth/register` - Register a new user

### Orders

- `POST /api/v1/orders/` - Create a new order
- `GET /api/v1/orders/user/` - Get a user's orders

### Users

- `GET /api/v1/users/me` - Get the current user
- `PUT /api/v1/users/me` - Update the current user

## Debugging API Requests

The backend provides detailed API documentation at http://localhost:8000/docs when running in development mode.
