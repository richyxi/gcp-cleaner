FROM python:3.9.1-alpine3.13

RUN apk --update add --no-cache g++

RUN pip install pandas

WORKDIR /home/

RUN mkdir in out schema

COPY run.py ./

CMD ["python3", "/home/run.py"]
