install:
	# install the dependencies
	pip install --upgrade pip &&\
	pip install -r requirements.txt
format:
	# format the code
	yapf *.py src/*.py tests/*.py
lint:
	# see flake8.ini for linting configuration
	flake8 -v *.py src/*.py tests/*.py
test:
	# see pytest.ini for test configuration
	python -m pytest -v --cov=src --cov=main.py tests/*.py
build:
	# build the container
	docker build -t fastapi-wiki .
run:
	# deploy the code
	docker run \
		--rm -d -p 8080:8080 \
		--name fastapi-wiki-container \
		-e CONTAINER_NAME \
		--env CONTAINER_NAME="fastapi-wiki-container" \
		--env-file .env \
		fastapi-wiki
deploy:
	# customise to the cloud provider
	build
	run
	push

all: install format lint test build run deploy