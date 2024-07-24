FROM python:3.12.2-slim

WORKDIR /ch0

COPY requirements.txt /ch0/requirements.txt
COPY api-mystery.db /ch0/api-mystery.db

RUN pip install --no-cache --no-cache-dir --no-deps -r /ch0/requirements.txt

COPY /ch0 /ch0

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
