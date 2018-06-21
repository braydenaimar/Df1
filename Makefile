
# Compiler
CC=gcc

# Compiler Options
CFLAGS=-Wall -c

# Linker Options
LDFLAGS=-Wall

all: daemon

# Link Files
daemon: calc_address.o common.o df1.o main.o read_A2.o read_boolean.o read_float.o read_integer.o read_socket.o select_fnct.o serial.o server.o write_AA.o write_AB.o write_boolean.o write_float.o write_integer.o
	$(CC) $(LDFLAGS) calc_address.o common.o df1.o main.o read_A2.o read_boolean.o read_float.o read_integer.o read_socket.o select_fnct.o serial.o server.o write_AA.o write_AB.o write_boolean.o write_float.o write_integer.o -o daemon

# Compile Dependencies
calc_address.o: calc_address.c df1.h
	$(CC) $(CFLAGS) calc_address.c

common.o: common.c df1.h
	$(CC) $(CFLAGS) common.c

df1.o: df1.c df1.h
	$(CC) $(CFLAGS) df1.c

main.o: main.c df1.h
	$(CC) $(CFLAGS) main.c

read_A2.o: read_A2.c df1.h
	$(CC) $(CFLAGS) read_A2.c

read_boolean.o: read_boolean.c df1.h
	$(CC) $(CFLAGS) read_boolean.c

read_float.o: read_float.c df1.h
	$(CC) $(CFLAGS) read_float.c

read_integer.o: read_integer.c df1.h
	$(CC) $(CFLAGS) read_integer.c

read_socket.o: read_socket.c df1.h
	$(CC) $(CFLAGS) read_socket.c

select_fnct.o: select_fnct.c df1.h
	$(CC) $(CFLAGS) select_fnct.c

serial.o: serial.c df1.h
	$(CC) $(CFLAGS) serial.c

server.o: server.c df1.h
	$(CC) $(CFLAGS) server.c

write_AA.o: write_AA.c df1.h
	$(CC) $(CFLAGS) write_AA.c

write_AB.o: write_AB.c df1.h
	$(CC) $(CFLAGS) write_AB.c

write_boolean.o: write_boolean.c df1.h
	$(CC) $(CFLAGS) write_boolean.c

write_float.o: write_float.c df1.h
	$(CC) $(CFLAGS) write_float.c

write_integer.o: write_integer.c df1.h
	$(CC) $(CFLAGS) write_integer.c
