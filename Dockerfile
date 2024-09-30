FROM python:3.9.20

RUN apt-get update && apt-get upgrade 
RUN useradd -ms /bin/bash cige
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

