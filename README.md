# 🌿 RootBound (Pure C Version) - Complete Guide

Welcome to RootBound. This document serves as the definitive guide for this project. It is divided into two halves: the first half explains everything in simple, non-technical language, and the second half explains the same details using professional software engineering terms.

---

## 🌟 Part 1: The Simple Explanation (For Everyone)

### What is RootBound?
RootBound is a 2D adventure game. Imagine a character walking around a world, interacting with things, and exploring. The "Pure C" part means the game is written in a very fundamental language that talks directly to your computer's brain (the CPU) without any "middleman" software slowing it down.

### How the Game Actually Works (Step-by-Step)
1. **The Heartbeat (The Loop):** The game runs in a circle, thousands of times per second.
   - It asks: "Is the player pressing a key?"
   - It calculates: "If the player moved right, are they hitting a wall?"
   - It draws: "Clear the screen and draw the character in the new position."
   - Then it repeats this instantly. This is why the game feels smooth.

2. **The Graphics (Raylib):** Since C doesn't know how to "draw a picture" by itself, we use a tool called **Raylib**. Think of Raylib as a giant box of crayons and a canvas that the C code uses to paint the game on your screen.

3. **The Memory (The Storage):** Most modern games (like Minecraft or Fortnite) have an automatic "cleaning crew" (called Garbage Collection) that deletes old data. RootBound doesn't have one. The programmer must manually tell the computer: "I am done with this piece of memory, you can have it back now." If we forget to do this, the game will "leak" memory and eventually crash.

### How to actually play it on your PC
Because this isn't a finished `.exe` app you download from a store, you have to "build" it. 
- You download the **Code** (the instructions).
- You use a **Compiler** (the translator) to turn those instructions into a file your Windows PC understands.
- You provide the **Library** (Raylib), which provides the tools to make the images appear.

---

## ⚙️ Part 2: The Technical Documentation (For Developers)

### Core Architecture
RootBound is implemented in **C99** leveraging the **Raylib** library for hardware-accelerated 2D rendering via OpenGL.

#### 1. The Game Loop (The Main Execution Cycle)
The engine operates on a synchronous `While` loop. Every iteration consists of three distinct phases:
- **Input Polling:** Utilizing `IsKeyDown()` and `IsKeyPressed()` from the Raylib API to capture user input from the keyboard/gamepad.
- **State Update:** The physics and logic layer. This handles coordinate translation, AABB (Axis-Aligned Bounding Box) collision detection, and entity state machine transitions.
- **Render Phase:** The `BeginDrawing()` and `EndDrawing()` block. The screen is cleared using `ClearBackground()`, and textures are blitted to the screen using `DrawTextureRec()`.

#### 2. Memory Management & Data Structures
To ensure zero-latency and high cache efficiency, the project avoids high-level abstractions:
- **Manual Allocation:** All dynamic memory is handled via `malloc()` and `free()`. Assets (textures, sounds) are loaded into VRAM at startup and explicitly unloaded at shutdown to prevent memory leaks.
- **Struct-Oriented Design:** Instead of Classes (which C doesn't have), we use `structs` to encapsulate entity data (e.g., `Player` struct containing `Vector2 position`, `float speed`, `Rectangle bounds`).
- **Pointer Arithmetic:** Used for efficient array traversal and manipulating game entities in the game world.

#### 3. Compilation & Linking Process
The project uses a **Makefile** to manage the build pipeline. The process is as follows:
- **Preprocessing:** Handling `#include` directives and `#define` macros.
- **Compilation:** Converting `.c` files into object files (`.o`) using the `gcc` compiler with optimization flag `-O3`.
- **Linking:** The linker combines the object files with the `raylib.lib` (or `.a`) static library to produce the final binary executable.

### Detailed Directory Breakdown
- `src/`: contains the implementation logic. 
    - `main.c`: Entry point, initializes the window and the main loop.
    - `player.c`: Logic for movement, animation, and input.
    - `world.c`: Handles map rendering and environment collisions.
- `include/`: contains the `.h` (header) files. These act as "contracts" that tell other parts of the program what functions and structs are available.
- `assets/`: Raw binary data (PNGs, WAVs) loaded into RAM at runtime.
- `Makefile`: The script that tells `make` exactly how to compile the code without typing long commands every time.

---

## 🛠 Troubleshooting & Debugging
- **Undefined Reference Errors:** This occurs if the linker cannot find the Raylib library files. Ensure `-lraylib` is present in the Makefile.
- **Segmentation Faults (Crash):** Occurs when the program tries to access a memory address it doesn't own (Null Pointer). This is usually fixed by checking if `malloc` returned `NULL`.
- **Asset Not Found:** Ensure the working directory is set to the project root, otherwise `LoadTexture()` will fail to find the path to the images.
