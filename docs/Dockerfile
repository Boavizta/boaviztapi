FROM python:3.7-slim-buster

WORKDIR /docs

RUN pip install mkdocs
RUN pip install mkdocs-render-swagger-plugin

COPY . .


EXPOSE 8080

ENTRYPOINT ["mkdocs", "serve"]
