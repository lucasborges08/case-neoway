FROM python:3.8-buster
RUN apt-get update -y && pip3 install gunicorn
COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt

EXPOSE 8088
CMD ["gunicorn", "-b", "0.0.0.0:8088", "-w", "1", "--timeout", "10", "app.main:api"]
