CXX=g++
CFLAGS=-std=c++20 -O2
OBJS=set.o

main.out: $(OBJS) $(source)
	$(CXX) $(CFLAGS) -o main.out $(OBJS) $(source)

set.o: Library/Namespace.hpp Library/Namespace.cpp
	$(CXX) $(CFLAGS) -c -o namespace.o Library/set.cpp

clean:
	rm -f *.o *.out