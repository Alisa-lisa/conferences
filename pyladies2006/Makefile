.PHONY: run
run:
	rm -rf env
	python3 -m venv env
	env/bin/pip install -r requirements.txt
	env/bin/python app/app.py

.PHONY: docker-run
docker-run:
	docker build -t myapp . && docker run -p 5000:5000 --name pyladies-app myapp

.PHONY: clean
clean:
	docker container rm pyladies-app
	docker image rm myapp