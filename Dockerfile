FROM python:3
MAINTAINER "Janik Luechinger janik.luechinger@uzh.ch"

COPY . /pga
WORKDIR /pga

RUN apt-get -y update && apt-get -y upgrade
RUN pip install -U pip && pip install -r requirements.txt

ENTRYPOINT [ "python", "-m", "agent" ]

# Manual image building
# docker build -t pga-cloud-agent .
# docker tag pga-cloud-agent jluech/pga-cloud-agent
# docker push jluech/pga-cloud-agent
