FROM python:3.6-jessie
RUN pip install -r requirements.txt
ADD . /code
WORKDIR /code
CMD ["python", "rest_api/manage.py runserver 0.0.0.0:8000"]
