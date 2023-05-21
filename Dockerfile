###############################################################
# TO          BUILD: docker build --force-rm -t logistic-benchmark-image . 
# TO RUN ITERACTIVE: docker run -it logistic-benchmark-image
###############################################################

# Imagem base
FROM python:3.9

# Definir diretório de trabalho
WORKDIR /app

# Copiar os diretórios "benchmark" e "languages"
COPY benchmark benchmark
COPY languages languages

# Instalar o bash
RUN apt-get update && apt-get install -y bash

###########################################################
# PYTHON - CONFIGURATION - BEGIN
###########################################################

# Copiar arquivos de requisitos
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# Instalar dependências para suporte CUDA
RUN apt-get update && apt-get install -y --no-install-recommends \
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

# Instalar PyPy
RUN wget -O - https://downloads.python.org/pypy/pypy3.9-v7.3.11-linux64.tar.bz2 | tar -xj \
    && mv pypy3.9-v7.3.11-linux64 /opt/ \
    && ln -s /opt/pypy3.9-v7.3.11-linux64/bin/pypy /usr/local/bin/pypy

###########################################################
# PYTHON - CONFIGURATION - END
###########################################################


# Definir o comando padrão para abrir o prompt do Bash
CMD [ "bash" ]
