#include <unistd.h>
#include <stdio.h>

int main() {
	printf("Usuario - %d\n", getuid());
	printf("Usuario Efetivo - %d\n", geteuid());
	return 0;
}
