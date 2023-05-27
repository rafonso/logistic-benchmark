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
RUN apt install -y bash nano

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
RUN apt install -y lua5.1 lua-socket

###########################################################
# RUBY
###########################################################
RUN apt install -y ruby

###########################################################
# C compile
###########################################################
RUN g++ -o languages/c-logistic-benchmark/c-logistic-benchmark languages/c-logistic-benchmark/c-logistic-benchmark.c
RUN sed -Ei "s/(c-logistic-benchmark)\.exe/\1/" languages/c-logistic-benchmark/c.config.json

###########################################################
# RUST
###########################################################
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o rustup.sh && \
    sh rustup.sh -y 
# Configura o ambiente do Rust
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cargo build --manifest-path languages/rust-logistic-benchmark/Cargo.toml --release
# Remove extension "exe" from executable name in config.json file
RUN sed -Ei "s/(rust-logistic-benchmark)\.exe/\1/" languages/rust-logistic-benchmark/rust.config.json

###########################################################
# GO
###########################################################
RUN wget https://golang.org/dl/go1.19.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.19.linux-amd64.tar.gz && \
    rm go1.19.linux-amd64.tar.gz
ENV PATH="/usr/local/go/bin:${PATH}"
WORKDIR /app/languages/go-logistic-benchmark
RUN go build
WORKDIR /app
RUN sed -Ei "s/(go-logistic-benchmark)\.exe/\1/" languages/go-logistic-benchmark/go.config.json

###########################################################
# C#
###########################################################
RUN wget https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
RUN dpkg -i packages-microsoft-prod.deb
RUN apt update
RUN apt install -y apt-transport-https
RUN apt update
RUN apt install -y dotnet-sdk-6.0
RUN dotnet publish languages/cs-logistic-benchmark/cs-logistic-benchmark.sln \
    --configuration Release --output languages/cs-logistic-benchmark/
RUN sed -Ei "s/(cs-logistic-benchmark)\.exe/\1/" languages/cs-logistic-benchmark/cs.config.json

# Definir o comando padrão para abrir o prompt do Bash
CMD [ "bash" ]
