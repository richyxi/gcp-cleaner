# GCP-CLEANER
Source code for a docker image that clean file data based on the data types

# Motivation
If you will migrate to Big Query, often you will face issues about the integrity of the data that you send.
This image will detect mixed data in your file and asign a null value.

# How it works?
This image needs to know:

- FILENAME=file.txt
- SCHEMA=squema.json
- DELIMITER=\t
- HEADER=false
- SPLIT_ROWS=100000

You will send this as env vars.

Notes:

* This image use chunks for default, i recommend using 100000 rows as the size limit fo the chunk but this number depends on your system spec.
* The output file will be delimited with commas(,)

# Use with docker

* Make sure to create: in, out and schema directories  
* You will put the file in the "in" directory (kinda redundant)
* the result will be in "out"
* And put the squema in .. you guess it.

First pull the image

```
docker pull ricardotryit/file-cleaner
```

Run the Docker image

```
docker run --rm -v $(shell pwd)/in:/home/in/ -v $(shell pwd)/out:/home/out/ -v $(shell pwd)/schema:/home/schema/ --env-file=$(shell pwd)/.env ricardotryit/file-cleaner
```

Notes:
* You can use the make file in the repository and make everything above by just typing make pull and make run
