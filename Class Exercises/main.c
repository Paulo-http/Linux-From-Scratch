//
//  main.c
//  SO
//
//  Created by Paulo Henrique Leite on 22/09/16.
//  Copyright © 2016 Paulo Henrique Leite. All rights reserved.
//

#include <stdint.h>

#define LIN 25
#define COL 80

typedef struct {
    uint8_t attr;
    uint8_t code;
} value;

int lenght(char *s) {
    int len = 0;
    while(*s != 0) {
        s++;
        len++;
    }
    return len;
}

int main() {
    value v[2000];
    uint8_t attr = 0x00;
    int lin = 10;
    int col = 20;
    int letter = 0;
    int index = 0;
    char *str = "Bem Vindo!";
    
    for (int l=1; l<=LIN; l++) {
        for (int c=0; c<COL; c++) {
            index = (l-1)*COL + c;
            v[index].attr = attr;
            
            if (index >= (lin-1)*COL + col && letter < lenght(str)) {
                v[index].code = (int)str[letter];
                letter++;
            }
            else {
                v[index].code = 32;
            }
        }
    }
    
    return 0;
}