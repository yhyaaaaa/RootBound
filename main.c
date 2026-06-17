#include "raylib.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Forward declarations of our C functions
void transform_data(unsigned char *data, size_t data_len, const char *hw_key);
void get_system_id(char *buffer, size_t max_len);
int store_secret(const char *key, const char *value);
char* get_secret(const char *key);

int main() {
    InitWindow(800, 450, "RootBound - Pure C Edition");
    SetTargetFPS(60);

    char hw_id[128];
    get_system_id(hw_id, 128);

    char inputBuffer[256] = {0};
    char outputBuffer[256] = {0};
    int lettersCount = 0;

    while (!WindowShouldClose()) {
        // Basic GUI logic
        BeginDrawing();
        ClearBackground(RAYWHITE);
        
        DrawText("RootBound: C-CORE GUI", 20, 20, 20, DARKGRAY);
        DrawText(TextFormat("Hardware ID: %s", hw_id), 20, 50, 10, GRAY);
        
        DrawText("Enter Secret:", 20, 100, 20, BLACK);
        DrawRectangle(20, 130, 300, 40, LIGHTGRAY);
        DrawText(inputBuffer, 30, 140, 20, MAROON);

        if (IsKeyPressed(KEY_ENTER)) {
             // This is where the C-Core XOR happens
             unsigned char temp[256];
             memcpy(temp, inputBuffer, 256);
             transform_data(temp, strlen(inputBuffer), hw_id);
             
             // For simplicity in this C demo, we store it as a raw string
             store_secret("root_secret", (char*)temp);
             strcpy(outputBuffer, "Stored successfully!");
        }

        DrawText(outputBuffer, 20, 200, 20, BLUE);
        EndDrawing();
    }
    CloseWindow();
    return 0;
}
