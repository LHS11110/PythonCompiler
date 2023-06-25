CXX=g++
CFLAGS=-std=c++20 -O2
OBJS=namespace.o

main.out: $(OBJS) $(source)
	$(CXX) $(CFLAGS) -o main.out $(OBJS) $(source)

namespace.o: Library/Namespace.hpp Library/Namespace.cpp
	$(CXX) $(CFLAGS) -c -o namespace.o Library/Namespace.cpp

clean:
	rm -f *.o *.out