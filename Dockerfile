FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

COPY src .

EXPOSE 8000/tcp

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]