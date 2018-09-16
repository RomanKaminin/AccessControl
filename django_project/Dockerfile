FROM python:3.5-slim

# It`s setting for use superuser after start application.


# Install some necessary things.
RUN apt-get update && apt-get install -y curl

# Install our requirements.
WORKDIR /root/src/
ADD ./requirements /root/src
RUN pip3 install -U pip
RUN pip3 install -Ur requirements
ADD . /root/src
