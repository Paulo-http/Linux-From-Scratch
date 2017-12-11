//
//  main.c
//  SO
//
//  Created by Paulo Henrique Leite on 10/11/16.
//  Copyright © 2016 Paulo Henrique Leite. All rights reserved.
//

#import "single_process.h"
#import "multi_process.h"
#import "multi_thread.h"
#include "helpers.h"

int main () {
    int choice = 0;
    
    while (1) {
        printf("\nChoice a function:\n");
        printf("1 - func estimate_pi_with_single_process\n");
        printf("2 - func estimate_pi_with_multi_process\n");
        printf("3 - func estimate_pi_with_multi_thread\n");
        
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                estimate_pi_with_single_process();
                break;
            case 2:
                estimate_pi_with_multi_process();
                break;
            case 3:
                estimate_pi_with_multi_thread();
                break;
            default:
                printf("\nInvalide choice!\n");
                break;
        }
    }
    
    return 0;
}
