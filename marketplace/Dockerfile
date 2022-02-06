FROM python:3.7.6-slim-stretch
MAINTAINER George Vassos "georgios.vassos1@maersk.com"

WORKDIR /service/marketplace
COPY protobufs/ /service/protobufs/
COPY marketplace/ /service/marketplace/

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get install -y python-pip && \
    /usr/local/bin/python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/recommendations.proto

EXPOSE 5000
ENV FLASK_APP=marketplace.py
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
