# Nome da DLL/SO
TARGET = libGenerateSeriesNative

# Diretório de saída
OUTPUT_DIR = ../target/native

# Configuração do compilador
CC = gcc
CFLAGS = -shared -o $(OUTPUT_DIR)/$(TARGET).so

# Diretórios de inclusão do JNI
JNI_INCLUDES = -I$(JAVA_HOME)/include -I$(JAVA_HOME)/include/linux

# Arquivos de origem
SRCS = generateSeries.c

# Geração da DLL/SO
all:
	$(CC) $(CFLAGS) $(JNI_INCLUDES) $(SRCS)
