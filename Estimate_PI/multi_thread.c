//
//  multi_thread.c
//  SO
//
//  Created by Paulo Henrique Leite on 17/11/16.
//  Copyright © 2016 Paulo Henrique Leite. All rights reserved.
//

#include "multi_thread.h"
#include "helpers.h"

pthread_mutex_t main_queue_mutex = PTHREAD_MUTEX_INITIALIZER;

int global_darts = 0;
int global_hit = 0;
int threads = 0;

void* extension_estimate_pi() {
    point p;
    double hit = 0.0;
    int darts = global_darts/threads;
    
    srand((unsigned)time(NULL));
    
    for (int i = 0; i<darts; i++) {
        p = randPoint();
        if (inside(p)) {
            hit++;
        }
    }
    
    pthread_mutex_lock (&main_queue_mutex);
    global_hit += hit;
    pthread_mutex_unlock (&main_queue_mutex);
    
    return NULL;
}

void estimate_pi_with_multi_thread() {
    printf("Enter with number of threads (minimum value: 2):\n");
    scanf("%d", &threads);
    if (threads < 2) {
        threads = 2;
    }

    printf("Enter with number of darts to be played (minimum value: 10000):\n");
    scanf("%d", &global_darts);
    if (global_darts < 10000) {
        global_darts = 10000;
    }
    
    for (int i = 0; i < threads; i++) {
        void* ret = NULL;
        pthread_t main_queue;
        pthread_create(&main_queue, NULL, &extension_estimate_pi, NULL);
        pthread_join(main_queue, &ret);
    }
    
    printf("global_hit: %d\n", global_hit);
    printf("global_darts: %d\n", global_darts);
    
    double pi = 4.0*global_hit/global_darts;
    printf("PI: %f\n", pi);
    
}
