FROM python:3.12

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install . --no-cache-dir 

COPY ./src /code/src

COPY ./service_account.json .

COPY ./files_storage /files_storage

ENV PYTHONPATH=/code/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
