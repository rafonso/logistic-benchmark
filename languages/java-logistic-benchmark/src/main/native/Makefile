# Source: https://makefiletutorial.com/, https://www.baeldung.com/jni

MSVC_DIR = 'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.30.30705\'
CC = ${MSVC_DIR}/bin/Hostx64/x64/cl.exe

all:
	${CC} -c \
	-I'${JAVA_PATH}'/include/win32 -I'${JAVA_PATH}'/include -I'${JAVA_PATH}'\include\bridge -I${MSVC_DIR}/include \
	generateSeries.c