ARG PY_VERSION=3.14
FROM python:$PY_VERSION-slim

WORKDIR /docs

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENTRYPOINT ["mkdocs", "serve"]
