FROM python:3.8.2
ENV HOME /root
WORKDIR /root
COPY . /root
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN pip install -r requirements.txt
RUN chmod +x /wait
EXPOSE 8080
CMD /wait && python3 server/pyserver.py