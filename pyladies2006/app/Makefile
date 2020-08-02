.PHONY: setup
setup:
	rm -rf env
	python3 -m venv env
	env/bin/pip install -r requirements.txt

.PHONY: docker-run
docker-run:
	docker-compose up -d --build postgres
	sleep 3
	docker-compose up --build app
