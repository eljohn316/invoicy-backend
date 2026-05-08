# `Invoicy API`

## Description

This project provides a RESTful API for an invoicing application. It allows users to create, manage, and track invoices through a set of well-defined endpoints.

## Motivation

This project originated from a [Frontend Mentor challenge](https://www.frontendmentor.io/challenges/invoice-app-i7KaLTQjl), to which I added additional features to enhance functionality. The primary motivation was to learn FastAPI and build a robust backend service to support a frontend invoicing application.

## Technology Stack

- [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
- [**SQLAlchemy**](https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- [**Pydantic**](https://docs.pydantic.dev) used by FastAPI, for the data validation and settings management.
- [**SQLite**](https://sqlite.org/index.html) as the development SQL database.
- [**PostgreSQL**](https://www.postgresql.org) as the production SQL database.
- [**AWS EC2**](https://aws.amazon.com/pm/ec2/) for deployment.

## Quick Start

1. Clone the repository:

   ```bash
   $ git clone <repository-url>
   $ cd invoice-app/backend
   ```

2. Install dependencies with uv:

   ```bash
   $ uv sync
   ```

3. Set up the database:
   - Configure your database settings in `src/config.py`
   - Run database migrations if applicable

## Usage

1. Start the FastAPI server:

   ```bash
   $ fastapi dev src/main.py
   ```

2. Access the API documentation at `http://localhost:8000/docs`

## Links

- [API Documentation]()
- [Frontend Demo]()
- [Frontend Repo]()

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
