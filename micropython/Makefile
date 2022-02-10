DB_PATH ?= $(shell echo "database/db.json")
.EXPORT_ALL_VARIABLES:

run_server:
	python recommendations/recommendations.py
.PHONY: run_server

run_client:
	FLASK_APP=marketplace/marketplace.py flask run
.PHONY: run_client
