#include <string>
#include <iostream>
#include <amqpcpp.h>

int
main(int argc, char **argv)
{
	AMQP::OutBuffer buffer(16);
	buffer.add("Hello, World!");
	std::cout << buffer.data() << std::endl;
	return 0;
}
