# docker build -t ubuntu1604py36
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y g++ bash m4 python-dev perl nodejs make wget musl-dev findutils coreutils grep tar gzip
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv libssl-dev libffi-dev python-dev
RUN apt-get install -y git
RUN apt-get upgrade -y gcc
#RUN apt-get upgrade -y gnu-gcc

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

RUN pip install numpy scikit-learn pandas scipy

WORKDIR /
RUN ls -l
RUN git clone https://github.com/eloaf/mmit.git
WORKDIR /mmit/
RUN python3.6 setup.py install 

RUN mkdir /home/code/

WORKDIR /home/code/
