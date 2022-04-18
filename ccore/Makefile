# Makefile template for a shared library in C
# https://www.topbug.net/blog/2019/10/28/makefile-template-for-a-shared-library-in-c-with-explanations/

CC = gcc  # C compiler
CFLAGS = -fPIC -Wall -Wextra -O2 -g -c # C flags
ifeq ($(OS), Windows_NT)
	LIB_DIR = vendors/webp/lib_msys
	LIB_FILE_PATTERN = libwebp*.a
else
	LIB_DIR = /usr/local/lib
	LIB_FILE_PATTERN = libwebp*.dll.a
endif
LIBS = $(wildcard $(LIB_DIR)/$(LIB_FILE_PATTERN))
LDFLAGS = -shared   # linking flags
RM = rm -f   # rm command
TARGET_LIB = release/libtridentframe_cf.so  # target lib

SRCS = tridentframe_cf.c  # source files
OBJS = $(SRCS:.c=.o)

.PHONY: all
all: ${TARGET_LIB}

$(TARGET_LIB): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

$(OBJS):
	$(CC) $(CFLAGS) ${SRCS} -o $@

.PHONY: clean
clean:
	-${RM} ${TARGET_LIB} $(OBJS)

.PHONY: again
again: clean all
