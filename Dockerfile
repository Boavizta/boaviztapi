ARG PY_VERSION=3.13

#---------------------------------------------------------------------------------------
# Stage 1 →  Builder image
#---------------------------------------------------------------------------------------
FROM python:$PY_VERSION-slim AS build-env

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir --upgrade poetry

# Copy project files and build wheel
COPY pyproject.toml poetry.lock ./
COPY . .
RUN poetry build --format wheel

#---------------------------------------------------------------------------------------
# Stage 2 →  Lambda runtime image
#---------------------------------------------------------------------------------------
FROM public.ecr.aws/lambda/python:$PY_VERSION AS lambda-env

ARG PY_VERSION=3.13

# Copy the built wheel from build stage, install, and clean up
COPY --from=build-env /app/dist/*.whl ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir --no-compile ${LAMBDA_TASK_ROOT}/*.whl && \
    rm ${LAMBDA_TASK_ROOT}/*.whl && \
    rm -rf /root/.cache

# Copy pyproject.toml for version info
COPY --from=build-env /app/pyproject.toml /var/lang/lib/python${PY_VERSION}/site-packages/boaviztapi/

# Set the handler
CMD ["boaviztapi.main.handler"]

#---------------------------------------------------------------------------------------
# Stage 3 →  Runtime image
#---------------------------------------------------------------------------------------
FROM python:$PY_VERSION-alpine AS run-env

# Python 3 surrogate unicode handling
# @see https://click.palletsprojects.com/en/7.x/python3/
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

ARG PY_VERSION=3.13
WORKDIR /app

# Copy wheel, install, and clean up in single layer
COPY --from=build-env /app/dist/*.whl /app/
RUN pip install --no-cache-dir --no-compile /app/*.whl && \
    rm /app/*.whl && \
    rm -rf /root/.cache

# Required in main.py
COPY --from=build-env /app/pyproject.toml /usr/local/lib/python$PY_VERSION/site-packages/boaviztapi/

EXPOSE 5000
CMD ["uvicorn", "boaviztapi.main:app", "--host", "0.0.0.0", "--port", "5000"]
