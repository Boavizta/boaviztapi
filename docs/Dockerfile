ARG PY_VERSION=3.13
FROM python:$PY_VERSION-slim

WORKDIR /docs

RUN pip install mkdocs \
  mkdocs-render-swagger-plugin \
  mkdocs-macros-plugin \
  mkdocs-material

COPY . .

EXPOSE 8080

ENTRYPOINT ["mkdocs", "serve"]
