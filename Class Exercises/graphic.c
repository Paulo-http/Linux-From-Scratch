#include <stdint.h>
#include <stdio.h>

typedef struct {
	uint8_t attr;
	uint8_t ascii;
} data;


int main() {
	int lines = 25;
	int column = 80;
	int attr = 0x0F;
	int lin = 10;
	int col = 20;
	char *text = "SUCESS";
	FILE *file = fopen("graphic.bin", "wb");

	data matrix[column * lines];
	for (int i = 0; i < column * lines; i++) {
		matrix[i].attr = 0x00;
		matrix[i].ascii = 0x00;
	}
	
	int i = lin * col;	
	for (int i = 0; text[i] != '\0'; i++) {
		matrix[i].attr = attr;
		matrix[i].ascii = text[i];

		if (i < lines * column) {
			i++;
		} else {
			i = 0;
		}
	}	

	fwrite(matrix, sizeof(matrix), 1, file); 

	return 0;
}