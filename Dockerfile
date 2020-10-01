FROM python:3.8.3-alpine3.11

ARG GRAVITEEIO_CLI_VERSION=0.1

RUN echo $GRAVITEEIO_CLI_VERSION
RUN pip install --upgrade pip
RUN pip install --no-cache-dir graviteeio-cli==${GRAVITEEIO_CLI_VERSION}

ENV GRAVITEEIO_CONF_FILE=/graviteeio/config/.graviteeio
VOLUME [ "/graviteeio/config/" ]

CMD ["/usr/local/bin/gio"]
