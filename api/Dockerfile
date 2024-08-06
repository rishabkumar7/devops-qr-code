FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]