FROM alpine
COPY quickstart.sh /
ENTRYPOINT ["sh", "/quickstart.sh"]