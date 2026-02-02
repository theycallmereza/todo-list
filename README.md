# FastAPI Todo List API

A modern FastAPI-based Todo List API with async SQLAlchemy, Alembic migrations, and code quality tools.

## Features

- ✅ FastAPI with async/await support
- ✅ SQLAlchemy 2.0 with async sessions
- ✅ Alembic for database migrations
- ✅ Pydantic for request/response validation
- ✅ Environment-based configuration with pydantic-settings
- ✅ Code formatting with Black
- ✅ Linting with Ruff
- ✅ Pre-commit hooks

## Project Structure

```
todo-list/
├── alembic/               # Database migrations
│   ├── versions/          # Migration files
│   └── env.py             # Alembic configuration
├── app/                   # FastAPI backend
│   ├── api/
│   │   └── v1/            # API version 1
│   ├── core/              # Settings, DB, security
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic schemas
│   └── main.py            # FastAPI application
├── frontend/              # Next.js + shadcn + RHF frontend
│   ├── package.json
│   ├── next.config.mjs
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── src/
│       ├── app/           # Next.js app router pages
│       └── components/    # UI components (shadcn style)
├── .env                  # Environment variables (not in git)
├── .gitignore
├── .pre-commit-config.yaml
├── alembic.ini
├── pyproject.toml        # Black & Ruff configuration
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd todo-list
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file in the root directory:

```bash
DATABASE_URL=sqlite+aiosqlite:///./todo.db
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### 7. Frontend (Next.js + shadcn + React Hook Form)

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000` and talks to the FastAPI backend at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Tasks

- `GET /tasks/` - Get all tasks
- `GET /tasks/{task_id}` - Get a single task by ID
- `POST /tasks/` - Create a new task

## Development

### Code Formatting

```bash
# Format code with Black
black app/

# Lint and fix with Ruff
ruff check app/ --fix

# Or use the helper script
./format.sh
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Check current migration status
alembic current
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

## Key FastAPI Concepts Demonstrated

1. **Routers**: Organized API endpoints using `APIRouter`
2. **Dependency Injection**: Database sessions via `Depends(get_db)`
3. **Pydantic Models**: Request/response validation with `TaskIn` and `TaskOut`
4. **Async/Await**: Async database operations with SQLAlchemy
5. **Path Parameters**: Dynamic routes like `/tasks/{task_id}`
6. **Error Handling**: `HTTPException` for proper status codes
7. **Status Codes**: Explicit HTTP status codes (201 Created, 404 Not Found)

## Technologies Used

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - Async ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **aiosqlite** - Async SQLite driver
- **Black** - Code formatter
- **Ruff** - Fast Python linter

## License

MIT
