FROM alpine:3.9
MAINTAINER Atila Aloise de Almeida


RUN apk add --update python3 shadow && \
    rm -rf /var/cache/apk/* && \
    pip3 install flask flask-jsonpify flask-restful datetime


RUN groupadd -g 1005 appuser && \
    useradd -r -u 1005 -g appuser appuser

USER appuser


COPY apiserver.py /apiserver.py
COPY test_api.py /test_api.py

EXPOSE 5000
# start
CMD python3 -m unittest && python3 apiserver.py
