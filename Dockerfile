
#pipenv lock --requirements > requirements.txt

# docker build -t registry.inviou.co/encryption:1.0.0 .
# docker push registry.inviou.co/encryption:1.0.0
#docker build -t registry.inviou.co/encryption:1.0.1 . && docker push registry.inviou.co/encryption:1.0.1

FROM tiangolo/uwsgi-nginx-flask:python3.7

MAINTAINER Or Lavee "or.lavee@inviou.com"
RUN  pip3 install pipenv

# COPY Pipfile* /app/

COPY . /app
RUN cd /app && pipenv lock --requirements > requirements.txt
RUN pip3 install -r /app/requirements.txt
# RUN pip install /app
EXPOSE 5000



