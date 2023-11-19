FROM python:3.9-slim AS build-env

ARG VERSION

COPY . /app

WORKDIR /app

RUN python -m pip install --upgrade poetry wheel twine
RUN poetry install --with dev
RUN poetry build
RUN PROJECT_VERSION=$(poetry version -s) && cp /app/dist/boaviztapi-$PROJECT_VERSION.tar.gz ./boaviztapi-$VERSION.tar.gz
RUN pip install boaviztapi-$VERSION.tar.gz && cp $(which uvicorn) /app

FROM gcr.io/distroless/python3
# Python 3 surrogate unicode handling
# @see https://click.palletsprojects.com/en/7.x/python3/
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY --from=build-env /app /app
COPY --from=build-env /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages

WORKDIR /app

EXPOSE 5000
CMD ["./uvicorn", "boaviztapi.main:app", "--host", "0.0.0.0", "--port", "5000"]
