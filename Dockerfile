FROM alpine
COPY quickstart.sh /
CMD ["/quickstart.sh"]
ENTRYPOINT ["sh", "/quickstart.sh"]