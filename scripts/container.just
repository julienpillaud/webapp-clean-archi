# PostgreSQL
db-postgres container_name port env_file:
	docker run -d \
	--name {{container_name}} \
	-p {{port}}:5432 \
	--env-file {{env_file}} \
	--restart unless-stopped \
	postgres:latest

postgres-dev port="5433" env_file=".env":
    just db-postgres webapp-postgres-dev {{port}} {{env_file}}

postgres-test port="5432" env_file=".env.test":
    just db-postgres webapp-postgres-test {{port}} {{env_file}}

# MongoDB
db-mongo container_name port env_file:
	docker run -d \
	--name {{container_name}} \
	-p {{port}}:27017 \
	--env-file {{env_file}} \
	--restart unless-stopped \
	mongo:latest

mongo-dev port="27018" env_file=".env":
	just db-mongo webapp-mongo-dev {{port}} {{env_file}}

mongo-test port="27017" env_file=".env.test":
	just db-mongo webapp-mongo-test {{port}} {{env_file}}

# RabbitMQ
rabbitmq port="5672" env_file=".env":
    docker run -d \
    --name rabbitmq \
    -p {{port}}:5672 \
    -p 15672:15672 \
    --env-file {{env_file}} \
    --restart unless-stopped \
    rabbitmq:4-management
