FROM python:3.6-jessie
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "rest_api/manage.py runserver 0.0.0.0:8000"]
