FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1
RUN apt update && apt install -y pkg-config gcc \
    default-libmysqlclient-dev pkg-config
COPY . /server
WORKDIR /server
RUN python3 -m venv venv && . venv/bin/activate
RUN pip3 install -r requirements.txt
#CMD ["python3", "manage.py", "runserver", "43.200.136.184:8000"]
#CMD ["uwsgi", "-i", "/server/uwsgi.ini"]
#EXPOSE 8000
