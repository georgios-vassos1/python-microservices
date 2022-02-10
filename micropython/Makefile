run_server:
	export DB_PATH="database/db.json"
	python recommendations/recommendations.py
.PHONY: run_server

run_client:
	FLASK_APP=marketplace/marketplace.py flask run
.PHONY: run_client
