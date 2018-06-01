FROM python:3

VOLUME /app
WORKDIR /app
EXPOSE 8443

CMD ["./run.sh"]
