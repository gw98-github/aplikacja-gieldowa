FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "/app/app.py" ]