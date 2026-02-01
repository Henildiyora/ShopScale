# This script automates the setup for all microservices

SERVICES := auth_service order_service inventory_service payment_service product_service

.PHONY: install start stop clean

# 1. Initialize all projects at once
install:
	@echo "Initializing all microservices with uv..."
	@for service in $(SERVICES); do \
		echo "Setting up $$service..."; \
		cd $$service && uv init && uv venv && cd ..; \
	done
	@echo "All services are ready!"

# 2. Start the Docker Infrastructure
up:
	@echo "Starting Infrastructure (DBs + RabbitMQ)..."
	docker compose -f infra/docker/docker-compose.yml up -d
	@echo "Infrastructure is running."

# 3. Stop the Infrastructure
down:
	@echo "Stopping Infrastructure..."
	docker compose -f infra/docker/docker-compose.yml down

# 4. Check the status
status:
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"