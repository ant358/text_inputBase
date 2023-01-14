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
	# run the container networks and volumes in docker-compose.yml
	docker run \
		--name source_text_data_db \
		text_data_db
deploy:
	# customise to the cloud provider
	# docker login
	# docker tag text_data_db svgcant2022/text_ms:text_data_db
	# docker push svgcant2022/text-ms:text_data_db

all: install format lint test build run deploy