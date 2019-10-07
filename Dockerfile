
#pipenv lock --requirements > requirements.txt

FROM python:3

MAINTAINER Or Lavee "or.lavee@inviou.com"

RUN  pip3 install pipenv

COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY . /tmp/myapp
RUN pip install /tmp/myapp


# export FLASK_APP=daemon.py
# export FLASK_DEBUG=1

ARG app=daemon.py 
ARG debug=1

ENV FLASK_APP=$app 
ENV FLASK_DEBUG=$debug 


CMD flask run --host=0.0.0.0 

# COPY ./Pipfile.lock /


# ENTRYPOINT [ "pipenv" ]

# CMD [ "pipenv run ./run-encrypt-daemon.sh" ]
