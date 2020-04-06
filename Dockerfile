FROM python:3.6-alpine

EXPOSE 8000
VOLUME /app

ENV PYTHONUNBUFFERED 1

RUN apk upgrade --no-cache \
    && apk add --no-cache --update git \
    && apk add --no-cache --update curl gcc g++ \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip/wheels/*

WORKDIR /app

ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["runserver", "0.0.0.0:8000"]
