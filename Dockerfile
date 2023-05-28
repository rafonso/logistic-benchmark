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

###########################################################
# C compile
###########################################################
RUN g++ -o languages/c-logistic-benchmark/c-logistic-benchmark languages/c-logistic-benchmark/c-logistic-benchmark.c
RUN sed -Ei "s/(c-logistic-benchmark)\.exe/\1/" languages/c-logistic-benchmark/c.config.json

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
# RUST
###########################################################
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o rustup.sh && \
    sh rustup.sh -y && rm rustup.sh
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
RUN rm packages-microsoft-prod.deb
RUN dotnet publish languages/cs-logistic-benchmark/cs-logistic-benchmark.sln \
    --configuration Release --output languages/cs-logistic-benchmark/
RUN sed -Ei "s/(cs-logistic-benchmark)\.exe/\1/" languages/cs-logistic-benchmark/cs.config.json

###########################################################
# NODE.JS AND DENO
###########################################################
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt install -y nodejs
RUN npm install -g typescript@4.5.5
RUN curl -fsSL https://deno.land/x/install/install.sh | sh -s v1.19.1
ENV DENO_INSTALL="/root/.deno"
ENV PATH="$DENO_INSTALL/bin:$PATH"

###########################################################
# JAVA & MAVEN & JVM LANGUAGES
###########################################################
# Install helper packages and Open JDK
RUN apt-get update && apt-get install -y \
    gnupg2 \
    software-properties-common \
    openjdk-17-jdk

# Install Maven 3.8
RUN wget https://dlcdn.apache.org/maven/maven-3/3.9.2/binaries/apache-maven-3.9.2-bin.tar.gz && \
    tar xzf apache-maven-3.9.2-bin.tar.gz && \
    mv apache-maven-3.9.2 /opt/maven && \
    rm apache-maven-3.9.2-bin.tar.gz
ENV MAVEN_HOME=/opt/maven
ENV PATH="${MAVEN_HOME}/bin:${PATH}"

# Install Groovy 4.0
RUN curl -L "https://groovy.jfrog.io/artifactory/dist-release-local/groovy-zips/apache-groovy-binary-4.0.12.zip" -o groovy.zip && \
    unzip groovy.zip && \
    mv groovy-4.0.12 /opt/groovy && \
    rm groovy.zip
ENV GROOVY_HOME=/opt/groovy
ENV PATH="${GROOVY_HOME}/bin:${PATH}"
# Install Gradle 7.2
RUN wget https://services.gradle.org/distributions/gradle-7.2-bin.zip && \
    unzip gradle-7.2-bin.zip && \
    mv gradle-7.2 /opt/gradle && \
    rm gradle-7.2-bin.zip
ENV GRADLE_HOME=/opt/gradle
ENV PATH="${GRADLE_HOME}/bin:${PATH}"

# Install Clojure 1.10
RUN curl -O https://download.clojure.org/install/linux-install-1.10.3.839.sh && \
    chmod +x linux-install-1.10.3.839.sh && \
    ./linux-install-1.10.3.839.sh && \
    rm linux-install-1.10.3.839.sh
# Install Leiningen
RUN wget https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein && \
    chmod +x lein && \
    mv lein /usr/local/bin/

# Install Jython 2.7
RUN curl -L -o jython-installer-2.7.2.jar "https://search.maven.org/remotecontent?filepath=org/python/jython-installer/2.7.2/jython-installer-2.7.2.jar" && \
    java -jar jython-installer-2.7.2.jar -s -d /opt/jython && \
    rm jython-installer-2.7.2.jar
ENV JYTHON_HOME=/opt/jython
ENV PATH="${JYTHON_HOME}/bin:${PATH}"
RUN sed -Ei "s/java -jar c:\/java\/jython2\.7\.3\/jython\.jar/jython/" languages/python-logistic-benchmark/jython.config.json

# Java
RUN mvn install -f languages/java-logistic-benchmark/pom.xml 
# PENDING java native
# Kotlin
RUN mvn install -f languages/kotlin-logistic-benchmark/pom.xml
# Kotlin native
WORKDIR /app/languages/kotlin-native-logistic-benchmark
RUN gradle clean
RUN gradle build
RUN sed -Ei "s/(kotlin_native_logistic_benchmark)\.exe/\1.kexe/" kotlin-native.config.json
WORKDIR /app
# Scala
RUN mvn install -f languages/scala-logistic-benchmark/pom.xml 
# Clojure
WORKDIR /app/languages/clojure-logistic-benchmark
RUN lein uberjar
WORKDIR /app


# Definir o comando padrão para abrir o prompt do Bash
CMD [ "bash" ]
