CXX=g++
CFLAGS=-std=c++20
OBJS=namespace.o identifier.o

main.out: $(OBJS) $(source)
	$(CXX) $(CFLAGS) -o main.out $(OBJS) $(source)

namespace.o: Library/Namespace.hpp Library/Namespace.cpp
	$(CXX) $(CFLAGS) -c -o namespace.o Library/Namespace.cpp

identifier.o: Library/Identifier.hpp Library/Identifier.cpp
	$(CXX) $(CFLAGS) -c -o identifier.o Library/Identifier.cpp

clean:
	rm -f *.o *.out