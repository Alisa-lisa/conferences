.PHONY: setup
setup:
	rm -rf env
	python3 -m venv env
	env/bin/pip install -r requirements.txt

.PHONY: docker-run
docker-run:
	docker build -t myapp . && docker run -p 5000:5000 myapp
