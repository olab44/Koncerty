FROM python:3.12

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install . --no-cache-dir 

COPY ./src /code/src
COPY ./tests /code/tests

COPY ./service_account.json .

# ENV PYTHONPATH=/code/src
ENV PYTHONPATH=/code/src:$PYTHONPATH


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
