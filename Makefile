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
	python -m pytest tests/*.py
build:
	# build the container
	docker build -t text_data_db .
run:
	# deploy the code
	docker run \
		-d -p 8080:8080 \
		--name source_text_data_db \
		# pass the container name to the logging config file via env
		-e CONTAINER_NAME \
		--env CONTAINER_NAME="source_text_data_db" \
		--env-file .env \
		# local docker volumes
		--volume text_data_vol:/app/data \
		--volume text_data_logs:/app/logs \
		# docker bridge network
		--network text_data \
		text_data_db
deploy:
	# customise to the cloud provider
	# docker login
	# docker tag text_data_db svgcant2022/text_ms:text_data_db
	# docker push svgcant2022/text-ms:text_data_db

all: install format lint test build run deploy