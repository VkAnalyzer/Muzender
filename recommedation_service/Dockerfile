FROM python:3.6-jessie
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "recommendation_app.py"]
