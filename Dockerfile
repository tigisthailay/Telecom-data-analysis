FROM python:3.9

COPY requirements.txt /

RUN python3 -m pip install -r requirements.txt
WORKDIR /app
COPY . /app/
CMD [ "python3", "app.py" ]
