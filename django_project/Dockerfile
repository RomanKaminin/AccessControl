FROM python:3.5-slim

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
#ENV PYTHONUNBUFFERED 1

# Install some necessary things.
#RUN apt-get update
#RUN apt-get install -y libpq-dev python3-dev memcached libmemcached-dev
#RUN apt-get install curl
# Install our requirements.
WORKDIR /root/src/
ADD ./requirements /root/src
RUN pip3 install -U pip
RUN pip3 install -Ur requirements
ADD . /root/src
#RUN echo yes | python manage.py collectstatic
#EXPOSE 8000
