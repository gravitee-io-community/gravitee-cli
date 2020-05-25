FROM python:3.8.3-alpine3.11

RUN pip install --upgrade pip
RUN pip install graviteeio-cli

ENV GRAVITEEIO_CONF_FILE=/graviteeio/config/.graviteeio
VOLUME [ "/graviteeio/config/" ]

CMD ["/usr/local/bin/gio"]
