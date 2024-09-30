FROM python:3.9.20-alpine

RUN apk update && apk upgrade 
RUN adduser -D cige
RUN mkdir /app

COPY requirements.txt /app/.
RUN pip install -r /app/requirements.txt
RUN rm /app/requirements.txt
COPY api.py /app/api.py

RUN chmod -R 750 /app
RUN chown -R root:cige /app 

USER cige
WORKDIR /app

EXPOSE 5000

CMD [ "python","/app/api.py" ]

