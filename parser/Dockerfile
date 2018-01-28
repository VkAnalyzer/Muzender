FROM python:3.6-jessie
RUN pip install -r requirements.txt
ADD . /code
WORKDIR /code
CMD ["python", "parser.py"]
