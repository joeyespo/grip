FROM ubuntu:16.04
MAINTAINER Xavier MARCELET <xavier@marcelet.com>

RUN apt-get update && apt-get install -y python-pip
RUN pip install --upgrade pip

COPY ./requirements-test.txt ./requirements.txt ./setup.py /tmp/grip/
COPY ./grip ./setup.py  /tmp/grip/grip/
RUN  cd /tmp/grip && python ./setup.py install && rm -rf /tmp/grip

RUN mkdir -p /export
COPY ./docker/entrypoint.sh /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
