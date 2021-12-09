FROM python:3.7-slim-buster

RUN pip install mkdocs
RUN pip install mkdocs-render-swagger-plugin

COPY /docs/ /docs/
WORKDIR /docs/

EXPOSE 8080

ENTRYPOINT ["mkdocs", "serve"]
