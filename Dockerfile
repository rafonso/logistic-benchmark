###############################################################
# TO          BUILD: docker build --force-rm -t logistic-benchmark-image . 
# TO RUN ITERACTIVE: docker run -v .\output:/app/output -it logistic-benchmark-image
###############################################################

# Image base
FROM python:3.9

# Define work directory
WORKDIR /app

# Copy directories "benchmark" e "languages"
COPY benchmark benchmark
COPY languages languages
VOLUME /app/output

# UPDATE & UPGRADE
RUN apt update && apt upgrade -y

# Install bash
RUN apt install -y bash

###########################################################
# PYTHON - CONFIGURATION - BEGIN
###########################################################

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# Install dependencies to support CUDA
RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    libz-dev \
    libbz2-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libgdbm-dev \
    zlib1g-dev \
    libreadline-dev \
    libncursesw5-dev \
    llvm \
    libncurses5 \
    libncursesw5 \
    libedit-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install PyPy
RUN wget -O - https://downloads.python.org/pypy/pypy3.9-v7.3.11-linux64.tar.bz2 | tar -xj \
    && mv pypy3.9-v7.3.11-linux64 /opt/ \
    && ln -s /opt/pypy3.9-v7.3.11-linux64/bin/pypy /usr/local/bin/pypy

###########################################################
# PYTHON - CONFIGURATION - END
###########################################################

RUN apt update

###########################################################
# LUA 5.1
###########################################################

RUN apt install -y lua5.1

###########################################################
# RUBY
###########################################################

RUN apt install -y ruby

###########################################################
# C compile
###########################################################

RUN g++ -o languages/c-logistic-benchmark/c-logistic-benchmark.exe languages/c-logistic-benchmark/c-logistic-benchmark.c

# Definir o comando padrão para abrir o prompt do Bash
CMD [ "bash" ]
