# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only dependency files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install

# Copy the rest of the project files
COPY . /app

# Ensure SQLAlchemy is available
RUN poetry run python -c "import sqlalchemy"

# Set the command to be configurable later
CMD ["poetry", "run", "python", "pipeline-scripts/main.py"]
