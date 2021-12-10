FROM python:3.7-slim-buster

RUN pip install mkdocs
RUN pip install mkdocs-render-swagger-plugin

WORKDIR /docs
COPY . .


EXPOSE 8080

ENTRYPOINT ["mkdocs", "serve"]
