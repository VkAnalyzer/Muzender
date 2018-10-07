FROM python:3.6-jessie
RUN mkdir /code
ADD requirements.txt /code
WORKDIR /code
RUN pip install -r requirements.txt
ADD . /code
CMD ["python3", "rest_api/manage.py runserver 0.0.0.0:8000"]
