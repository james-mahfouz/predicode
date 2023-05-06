FROM python:3.11

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR ./app

CMD [ "uvicorn", "main:app", "--port", "8000", "--reload" ]


