FROM python:3.9.20

RUN apt-get -y update && apt-get -y upgrade 

# FOR ORACLE DATABASE
RUN apt-get install -y libaio1 alien
RUN wget http://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/getPackage/oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
RUN alien -i --scripts oracle-instantclient*.rpm
RUN rm -f oracle-instantclient*.rpm 

RUN useradd -ms /bin/bash cige
RUN mkdir /app

COPY app/requirements.txt /app/.
RUN pip install -r /app/requirements.txt
RUN rm /app/requirements.txt
COPY app/*.py /app/.

RUN chmod -R 750 /app
RUN chown -R root:cige /app 

USER cige
WORKDIR /app

EXPOSE 5000

CMD [ "python","/app/api.py" ]

