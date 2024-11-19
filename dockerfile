# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY . /app

# Install dependencies
RUN poetry install

# Run the script
CMD ["poetry", "run", "python", "pipeline-scripts/main.py"]
