###############################################################
# TO BUILD: docker build --force-rm -f alpine.Dockerfile -t logistic-benchmark-image .
# TO RUN ITERACTIVE: docker run -v .\output:/app/output -it logistic-benchmark-image
###############################################################

# Image base
FROM python:3.10.12-alpine3.18

# Define work directory
WORKDIR /app

###########################################################
# 1 - Installations of libraries and dependencies
###########################################################

# UPDATE & UPGRADE
RUN apk update && apk upgrade

# Install necessary packages
RUN apk add --no-cache \
bash \
nano \
build-base \
openssl-dev \
libffi-dev \
bzip2-dev \
sqlite-dev \
ncurses-dev \
gdbm-dev \
zlib-dev \
gcompat \
readline-dev \
llvm \
libedit \
expat \
xz \
tk \
wget \
git \
# Install Lua 5.1
lua5.1 \
lua-socket \
# Install Ruby
ruby \
gnupg \
# Install helper packages and Open JDK
openjdk17 \
maven \
gradle \
clojure \
# Install .Net
dotnet6-sdk \
# Install Node & DEno
nodejs \
npm \
#    deno \
curl \
rust \
cargo \
go \
unzip \
# Python
tesseract-ocr \
python3-dev \
py3-numpy \
libc6-compat \
libgcc \
glib-dev \
jpeg-dev \
jq

# change default shell from ash to bash. Source: https://hub.docker.com/r/bashell/alpine-bash/dockerfile
RUN sed -i -e "s/bin\/ash/bin\/bash/" /etc/passwd
ENV export PS1='[\[\e[1m\]\t:\w\$\[\e[0m\]] '

# Install Python dependencies
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install tabulate matplotlib pyinstaller

# Install PyPy
ENV PYPY_VERSION=3.10-v7.3.12
RUN wget -O - https://downloads.python.org/pypy/pypy${PYPY_VERSION}-linux64.tar.bz2 | tar -xj && \
    mv pypy${PYPY_VERSION}-linux64 /opt/ && \
    ln -s /opt/pypy${PYPY_VERSION}-linux64/bin/pypy3 /usr/local/bin/pypy

# Install & configure Deno
RUN npm install -g typescript@4.5.5
RUN curl -fsSL https://deno.land/x/install/install.sh | sh -s v1.19.1
ENV DENO_INSTALL="/root/.deno"
ENV PATH="$DENO_INSTALL/bin:$PATH"

# Configure Java
ENV JAVA_HOME=/usr/lib/jvm/default-jvm

# Install Groovy 4.0
ENV GROOVY_VERSION=4.0.12
RUN curl -L "https://groovy.jfrog.io/artifactory/dist-release-local/groovy-zips/apache-groovy-binary-${GROOVY_VERSION}.zip" -o groovy.zip && \
    unzip groovy.zip && \
    mv groovy-${GROOVY_VERSION} /opt/groovy && \
    rm groovy.zip
ENV GROOVY_HOME=/opt/groovy
ENV PATH="${GROOVY_HOME}/bin:${PATH}"

# Install Leiningen
RUN wget https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein && \
    chmod +x lein && \
    mv lein /usr/local/bin/

# Install Jython 2.7
ENV JYTHON_VERSION=2.7.3
RUN curl -L -o jython-installer-${JYTHON_VERSION}.jar "https://search.maven.org/remotecontent?filepath=org/python/jython-installer/${JYTHON_VERSION}/jython-installer-${JYTHON_VERSION}.jar" && \
    java -jar jython-installer-${JYTHON_VERSION}.jar -s -d /opt/jython && \
    rm jython-installer-${JYTHON_VERSION}.jar
ENV JYTHON_HOME=/opt/jython
ENV PATH="${JYTHON_HOME}/bin:${PATH}"

# 2.1 - preload Java & JVM languages dependencies
# COPY .libs $HOME/root
COPY pre-load pre-load
# Preload Gradle daemon and Kotlin native - PENDING
# WORKDIR /app/pre-load/preload-kotlin-native
# RUN gradle build
# WORKDIR /app
# Preload Kotlin
RUN mvn install -f ./pre-load/preload-kotlin/pom.xml
# Preload Scala
RUN mvn install -f ./pre-load/preload-scala/pom.xml
# Clean pre-load
RUN rm -rf /app/pre-load

###########################################################
# 2 - Define COPY and VOLUME
###########################################################

COPY benchmark benchmark
COPY languages languages
VOLUME /app/output

###########################################################
# 3 - Compilations and tweaks within the directory /app/languages
###########################################################

# C compile
RUN g++ -O3 -o languages/c-logistic-benchmark/c-logistic-benchmark languages/c-logistic-benchmark/c-logistic-benchmark.c
RUN sed -Ei "s/(c-logistic-benchmark)\.exe/\1/" languages/c-logistic-benchmark/c.config.json

# Jython Native
RUN sed -Ei "s/c:\/java\/jython2.7.3\///" languages/python-logistic-benchmark/jython.config.json

# Python Native
WORKDIR /app/languages/python-logistic-benchmark
RUN pyinstaller -F main.py 
RUN sed -Ei "s/(main)\.exe/\1/" python-exe.config.json
WORKDIR /app

# Rust
RUN cargo build --manifest-path languages/rust-logistic-benchmark/Cargo.toml --release
# Remove extension "exe" from executable name in config.json file
RUN sed -Ei "s/(rust-logistic-benchmark)\.exe/\1/" languages/rust-logistic-benchmark/rust.config.json

# Go
WORKDIR /app/languages/go-logistic-benchmark
RUN go build
RUN sed -Ei "s/(go-logistic-benchmark)\.exe/\1/" go.config.json
WORKDIR /app

# C#
RUN dotnet publish languages/cs-logistic-benchmark/cs-logistic-benchmark.sln \
    --configuration Release --output languages/cs-logistic-benchmark/
RUN sed -Ei "s/(cs-logistic-benchmark)\.exe/\1/" languages/cs-logistic-benchmark/cs.config.json

# Node
WORKDIR /app/languages/typescript-node-logistic-benchmark
RUN npm install
WORKDIR /app

# Java
RUN mvn install -f languages/java-logistic-benchmark/pom.xml 
# Create Java native SO
WORKDIR /app/languages/java-logistic-benchmark/generate_series_native
RUN mkdir ../target/native
RUN sed -Ei "s/        /\t/" Makefile
RUN make
WORKDIR /app

# Kotlin
RUN mvn install -f languages/kotlin-logistic-benchmark/pom.xml

# Kotlin with native
RUN mvn install -f languages/kotlin-with-native-logistic-benchmark/pom.xml
# Create Kotlin native SO
WORKDIR /app/languages/kotlin-with-native-logistic-benchmark/generate_series_native
RUN mkdir ../target/native
RUN make
WORKDIR /app

# Kotlin native
WORKDIR /app/languages/kotlin-native-logistic-benchmark
# RUN gradle clean build
RUN sed -Ei "s/(kotlin_native_logistic_benchmark)\.exe/\1.kexe/" kotlin-native.config.json
WORKDIR /app

# Scala
RUN mvn install -f languages/scala-logistic-benchmark/pom.xml 

# Clojure
WORKDIR /app/languages/clojure-logistic-benchmark
RUN lein uberjar
WORKDIR /app

###########################################################
# 4 - Set default command to open Bash prompt
###########################################################

CMD [ "bash" ]
