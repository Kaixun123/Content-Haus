PROJECT_NAME = "content-haus"
LOCAL_DEPLOY_DIR = "./"

# ---------------------------------------
# For deploying docker containers locally
# ---------------------------------------
up:
	@docker compose -p ${PROJECT_NAME} \
		-f ${LOCAL_DEPLOY_DIR}/docker-compose.yml \
		up --build -d --remove-orphans

nobuild/up:
	@docker-compose -p ${PROJECT_NAME} \
		-f ${LOCAL_DEPLOY_DIR}/docker-compose.yml \
		up -d

# ---------------------------------
# For tearing down local deployment
# ---------------------------------
down:
	@docker compose -p ${PROJECT_NAME} \
		-f ${LOCAL_DEPLOY_DIR}/docker-compose.yml \
		down
down-clean:
	@docker compose -p ${PROJECT_NAME} \
		-f ${LOCAL_DEPLOY_DIR}/docker-compose.yml \
		down --remove-orphans
	@docker volume ls -q | grep -v grafana_data | xargs -r docker volume rm
	@docker system prune -f

prune-all:
	@echo "Running this command will prune all images. Do you want to proceed [y/N]?"; \
	read ans; \
	case "$$ans" in \
		[Yy]*) docker image prune -a -f ;; \
		*) echo "Aborting." ;; \
	esac

# -------------------
# Development targets
# -------------------
dev:
	@docker compose -p ${PROJECT_NAME} \
				    -f ${LOCAL_DEPLOY_DIR}/docker-compose.yml \
				    -f ${LOCAL_DEPLOY_DIR}/docker-compose.dev.yml \
				    up --build -d

nobuild/dev:
	@docker compose -p ${PROJECT_NAME} \
				    -f ${LOCAL_DEPLOY_DIR}/docker-compose.yml \
				    -f ${LOCAL_DEPLOY_DIR}/docker-compose.dev.yml \
				    up -d