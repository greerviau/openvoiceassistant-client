#!/bin/bash

apt update
apt install -y python3-pip python3.11-venv python3-pyaudio \
                git wget libatlas-base-dev libglib2.0-dev \
                libgirepository1.0-dev libcairo2-dev \
                gfortran gcc libopenblas-dev portaudio19-dev \
                libblas-dev llvm python3-scipy build-essential sox

CWD=$(pwd)

python3.11 -m venv $CWD/env

source $CWD/env/bin/activate
 
python3.11 -m pip install -r requirements.txt
