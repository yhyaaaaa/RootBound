#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void transform_data(unsigned char *data, size_t data_len, const char *hw_key) {
    size_t key_len = strlen(hw_key);
    if (key_len == 0) return;
    for (size_t i = 0; i < data_len; i++) {
        data[i] ^= hw_key[i % key_len];
    }
}

void get_system_id(char *buffer, size_t max_len) {
    FILE *fp = fopen("/sys/class/dmi/id/product_uuid", "r");
    if (fp == NULL) {
        strncpy(buffer, "UNKNOWN_HARDWARE_ID", max_len);
        return;
    }
    if (fgets(buffer, max_len, fp) != NULL) {
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len-1] == '\n') buffer[len-1] = '\0';
    }
    fclose(fp);
}
