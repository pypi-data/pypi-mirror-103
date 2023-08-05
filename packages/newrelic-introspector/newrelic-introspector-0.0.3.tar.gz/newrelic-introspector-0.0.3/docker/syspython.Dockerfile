FROM python:3.7

RUN mkdir -p /app/

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./src /app/

WORKDIR /app/

CMD ["/app/start.sh"]
