#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "tridentframe_cf.h"

char *ping() {
    char* msg = "PONG from tridentframe_cf.c";
    char* ping_msg = strdup(msg);
    // char* ping_msg = malloc(sizeof(char) * strlen(msg) + 1);
    // if(ping_msg == NULL) exit(1);
    // strcpy(ping_msg, msg);
    printf("original msg address: %p\n", msg);
    printf("ping_msg address: %p\n", ping_msg);
    return ping_msg;
}

void freeChar(char* ptr){
    printf("freeing address: %p\n", ptr);
    free(ptr);
}

int totalNumbers(uint8_t* numbers, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++){
        sum += numbers[i];
    }
    return sum; 
}
