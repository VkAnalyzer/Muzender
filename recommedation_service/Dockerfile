FROM python:3.6-jessie
VOLUME /data
RUN mkdir /code
ADD requirements.txt /code
WORKDIR /code
RUN pip install -r requirements.txt
ADD . /code
CMD ["python", "recommendation_app.py"]
