imageName := ricardotryit/file-cleaner:1.0.0

build:
	docker build -t $(imageName) .

push:
	docker push $(imageName)

run:
	docker run --rm -v $(shell pwd)/in:/home/in/ -v $(shell pwd)/out:/home/out/ -v $(shell pwd)/schema:/home/schema/ --env-file=$(shell pwd)/.env $(imageName)

interactive:
	docker run --rm -v $(shell pwd)/in:/home/in/ -v $(shell pwd)/out:/home/out/ -v $(shell pwd)/schema:/home/schema/ --env-file=$(shell pwd)/.env -ti --entrypoint="/bin/sh" $(imageName)

