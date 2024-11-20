# Define variables
IMAGE_NAME := crm_etl_pipeline
CONTAINER_NAME := crm_etl_pipeline_container
ENV_FILE := .env
DB_CONTAINER_NAME := crm-etl-pipeline-postgres-1
NETWORK := crm-etl-pipeline_crm_etl_pipeline

docker-exec:
	docker exec -it $(CONTAINER_NAME) poetry run python pipeline-scripts/main.py

# Build the Docker image
docker-build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
docker-run:
	docker run --network $(NETWORK) --env-file $(ENV_FILE) --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stop the running Docker container
docker-stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Rebuild and rerun the Docker container
rebuild: docker-stop docker-build docker-run

# Clean up dangling images and stopped containers
docker-clean:
	docker system prune -f

# Start dependencies
up-deps:
	docker-compose up -d

# Get local up and running
up:
	make docker-build
	make up-deps

# Stop local
down:
	docker-compose down

man-db:
	docker exec -it $(DB_CONTAINER_NAME) psql -h postgres -p 5432 -U rashmi -d crm

psql:
	psql -h localhost -p 5432 -U rashmi -d crm

.PHONY: docker-build docker-run docker-stop docker-rebuild docker-clean up up-deps down