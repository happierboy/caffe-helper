LIB=/usr/lib/x86_64-linux-gnu
INCLUDE=/usr/include
$(info $(LIB) $(INCLUDE)) 
test_gflags: main.o
	g++ -o $@ $^ -L$(LIB) -lgflags -lpthread

main.o: main.cpp
	g++ -c -o $@ $^ -I$(INCLUDE)
