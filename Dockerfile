FROM python:3.12

RUN mkdir /smart_calendar
WORKDIR /smart_calendar

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update

COPY . .

CMD uvicorn src.api.main:app --workers 4 --host 0.0.0.0 --port 80
