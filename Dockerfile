ARG PY_VERSION=3.13

#---------------------------------------------------------------------------------------
# Stage 1 → Builder image
#---------------------------------------------------------------------------------------
FROM python:$PY_VERSION-slim AS build-env

ARG VERSION
WORKDIR /app

# Install python deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir --upgrade poetry wheel twine

# Install project deps
COPY pyproject.toml poetry.lock ./
RUN poetry install --with dev --no-root

# Copy code *after* installing deps to avoid unnecessarily invalidating cache
COPY . .

# Build the project
RUN poetry build
RUN PROJECT_VERSION=$(poetry version -s) && \
    cp /app/dist/boaviztapi-$PROJECT_VERSION.tar.gz ./boaviztapi-$VERSION.tar.gz

#---------------------------------------------------------------------------------------
# Stage 2 → Runtime image
#---------------------------------------------------------------------------------------
FROM python:$PY_VERSION-slim AS run-env
# Python 3 surrogate unicode handling
# @see https://click.palletsprojects.com/en/7.x/python3/
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

ARG VERSION
WORKDIR /app

# Copy executable and dependencies
COPY --from=build-env /app/boaviztapi-$VERSION.tar.gz /app/
RUN pip install --no-cache-dir /app/boaviztapi-$VERSION.tar.gz

# Required in main.py
COPY --from=build-env /app/pyproject.toml /usr/local/lib/python3.13/site-packages/boaviztapi/

# Copy uvicorn executable
RUN pip install --no-cache-dir uvicorn

EXPOSE 5000
CMD ["uvicorn", "boaviztapi.main:app", "--host", "0.0.0.0", "--port", "5000"]
