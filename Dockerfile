FROM ubuntu:latest

RUN apt update && apt install -y python3-pip ssdeep libfuzzy-dev
COPY src /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD python3 main.py

