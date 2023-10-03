FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /project_FastAPI

COPY . .

RUN pip install -r requirements.txt


CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]