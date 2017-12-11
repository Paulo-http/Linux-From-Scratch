//
//  helpers.h
//  SO
//
//  Created by Paulo Henrique Leite on 17/11/16.
//  Copyright © 2016 Paulo Henrique Leite. All rights reserved.
//

#ifndef helpers_h
#define helpers_h

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
#include <sys/types.h> 
#include <unistd.h>
#include <pthread.h>
#include <signal.h>
#include <string.h> 
#include <sys/wait.h>

typedef struct point {
    double x;
    double y;
}point;

point randPoint();

double distance(point p1, point p2);

bool inside(point p);

#endif /* helpers_h */
