LIB=/usr/lib/x86_64-linux-gnu
INCLUDE=/usr/include
test_glog: main.o
	g++ -o $@ $^ -L$(LIB) -lglog -lpthread

main.o: main.cpp
	g++ -c -o $@ $^ -I$(INCLUDE)
