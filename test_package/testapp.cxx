#include <string>
#include <iostream>
#include <amqpcpp.h>

int
main(int argc, char **argv)
{
	const std::string s = "Hello, World!";
	AMQP::ByteBuffer buffer(s.data(), s.size());
	std::cout << buffer.size() << std::endl;
	return 0;
}
