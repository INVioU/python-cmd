
#pipenv lock --requirements > requirements.txt

# docker build -t registry.inviou.co/encryption:1.0.0 .
# docker push registry.inviou.co/encryption:1.0.0


FROM tiangolo/uwsgi-nginx-flask:python3.7

MAINTAINER Or Lavee "or.lavee@inviou.com"
RUN  pip3 install pipenv

# COPY Pipfile* /app/

COPY . /app
RUN cd /app && pipenv lock --requirements > requirements.txt
RUN pip3 install -r /app/requirements.txt
# RUN pip install /app
EXPOSE 5000





# MAINTAINER Or Lavee "or.lavee@inviou.com"

# RUN  pip3 install pipenv

# COPY Pipfile* /tmp/
# RUN cd /tmp && pipenv lock --requirements > requirements.txt
# RUN pip3 install -r /tmp/requirements.txt

# COPY . /tmp/myapp
# RUN pip install /tmp/myapp


# # export FLASK_APP=daemon.py
# # export FLASK_DEBUG=1

# ARG app=daemon.py 
# ARG debug=1

# ENV FLASK_APP=$app 
# ENV FLASK_DEBUG=$debug 


# CMD flask run --host=0.0.0.0 

# # COPY ./Pipfile.lock /


# # ENTRYPOINT [ "pipenv" ]

# # CMD [ "pipenv run ./run-encrypt-daemon.sh" ]
