CC=gcc
CFLAGS=-Wall -I.
LIBS=-lraylib -lsqlite3 -lm -lpthread -ldl

all: rootbound_c

rootbound_c: main.c core_engine.c database.c
	$(CC) $(CFLAGS) -o rootbound_c main.c core_engine.c database.c $(LIBS)

clean:
	rm -f rootbound_c
