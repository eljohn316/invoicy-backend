# `Invoicy API`

## Description

This project provides a RESTful API for an invoicing application. It allows users to create, manage, and track invoices through a set of well-defined endpoints.

## Motivation

This project originated from a [Frontend Mentor challenge](https://www.frontendmentor.io/challenges/invoice-app-i7KaLTQjl), to which I added additional features to enhance functionality. The primary motivation was to learn full‑stack development by building a complete invoicing application with React on the frontend (housed in a [separate repository](https://github.com/eljohn316/invoicy-frontend)) and FastAPI on the backend.

## Technology Stack

- [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
- [**SQLAlchemy**](https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- [**Pydantic**](https://docs.pydantic.dev) used by FastAPI, for the data validation and settings management.
- [**PostgreSQL**](https://www.postgresql.org) as SQL database.
- [**Docker**](https://www.docker.com/) for running a PostgreSQL container locally.
- [**AWS EC2**](https://aws.amazon.com/pm/ec2/) for deployment.

## Development

1. Clone the repository:

   ```bash
   $ git clone https://github.com/eljohn316/invoicy-backend
   $ cd invoice-backend
   ```

2. Install dependencies with uv:

   ```bash
   $ uv sync
   ```

3. Create .env

   ```python
   # Environment: local, staging, production
   ENVIRONMENT="local"
   SECRET_KEY="changethis"

   CORS_ORIGINS="http://localhost:5173,http://localhost:4173"

   POSTGRES_SERVER="localhost"
   POSTGRES_PORT="5432"
   POSTGRES_DB="invoicy"
   POSTGRES_USER="postgres"
   POSTGRES_PASSWORD="changethis"
   ```

4. Configure your database
   - If you have [Docker](https://www.docker.com/) installed in your local machine, you can just run a postgres container and you're all set up.

     ```bash
     $ docker compose up
     ```

   - You can also download postgres in your local machine. Follow the steps [here](https://www.postgresql.org/download/)

5. Create database tables

   ```bash
   $ uv run alembic upgrade head
   ```

6. Run the app
   ```bash
   $ fastapi dev
   ```

## Links

- [API Documentation URL](http://18.140.255.93:8000/docs)
- Frontend
  - [Live Demo URL](https://invoicy-five.vercel.app)
  - [Repository](https://github.com/eljohn316/invoicy-frontend)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
