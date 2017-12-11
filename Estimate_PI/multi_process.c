//
//  multi_process.c
//  SO
//
//  Created by Paulo Henrique Leite on 17/11/16.
//  Copyright © 2016 Paulo Henrique Leite. All rights reserved.
//

#include "multi_process.h"
#include "helpers.h"

sig_atomic_t child_exit_status;

void clean_up_child_process (int signal_number) {
    int status;
    wait (&status);
    child_exit_status = status;
}

void handle_SIGCHLD() {
    struct sigaction sigchld_action;
    memset (&sigchld_action, 0, sizeof (sigchld_action));
    sigchld_action.sa_handler = &clean_up_child_process;
    sigaction (SIGCHLD, &sigchld_action, NULL);
}

void extension_estimate_pi_with_multi_process() {
    point p;
    int forks;
    int darts;
    double hit = 0.0;
    pid_t forkable = 0;

    srand((unsigned)time(NULL));
    
    printf("Enter with number of forks (minimum value: 2):\n");
    scanf("%d", &forks);
    if (forks < 2) {
        forks = 2;
    }

    printf("Enter with number of darts to be played (minimum value: 10000):\n");
    scanf("%d", &darts);
    if (darts < 10000) {
        darts = 10000;
    }

    darts /= forks;
    
    for (int i = 0; i < forks; i++) {
        if (forkable == 0) {
            forkable = fork();
        }
    }
    
    for (int i = 0; i < darts; i++) {
        p = randPoint();
        if (inside(p)) {
            hit++;
        }
    }
    
    double pi = 4.0*hit/darts;
    
    printf("PI: %f\n", pi);
}

void estimate_pi_with_multi_process() {
    handle_SIGCHLD();
    extension_estimate_pi_with_multi_process();
}
