FROM python:3.6-jessie
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y curl python-software-properties
CMD ["curl",  "-sL https://deb.nodesource.com/setup_9.x | bash -"]
RUN apt-get install -y nodejs
CMD ["npm install && npm run build"]
CMD ["python3", "rest_api/manage.py runserver 0.0.0.0:8000"]
