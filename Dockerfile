FROM python:3

VOLUME /app
WORKDIR /app

CMD ["./run.sh"]
