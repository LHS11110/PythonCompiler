CC=gcc
CFLAGS=-g -Wall -Wextra -pedantic -Werror -target x86_64-apple-darwin20.3.0

all:
	nasm -f macho64 -o $(source).o $(source).asm
	$(CC) $(source).o -o $(source).out $(CFLAGS)
	rm $(source).o

clean:
	rm -f *.out *.o