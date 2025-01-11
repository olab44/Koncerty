FROM python:3.12

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install . --no-cache-dir 

COPY ./src /code/src
COPY ./tests /code/tests

COPY ./service_account.json .
COPY ./credentials.json .

# ENV PYTHONPATH=/code/src
ENV PYTHONPATH=/code/src:$PYTHONPATH


CMD ["sh", "-c", "if [ \"$APP_ENV\" = \"test\" ]; then coverage run -m uvicorn src.main:app --host 0.0.0.0 --port 8000; else uvicorn src.main:app --host 0.0.0.0 --port 8000; fi"]
