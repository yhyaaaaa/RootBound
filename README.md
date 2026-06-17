# 🌿 RootBound (Pure C Version)

RootBound is a top-down adventure game rewritten from the ground up in Pure C using the Raylib library. This version focuses on high performance, low memory overhead, and a clean architectural structure.

---

## 🎮 For the Players (The Simple Version)

### What is this?
This is a game where you explore a world, interact with the environment, and progress through an adventure. Unlike most modern games, this one is written in **C**, which is one of the fastest and oldest programming languages in the world.

### How to Run This Game on Windows
Since this is a "Pure C" project, you can't just run a `.exe` immediately; you have to "build" it first.

**1. Get the Tools:**
*   **w64devkit:** This is the "compiler." It translates the C code into a language your computer understands. [Download here](https://github.com/skeetele/w64devkit).
*   **Raylib:** This is the "graphics engine" that allows the game to draw images and handle sound. [Download here](https://www.raylib.com/).

**2. Setup:**
*   Download this repository as a ZIP file and extract it.
*   Ensure the Raylib `include` and `lib` folders are placed where the compiler can find them (usually in the same project folder).

**3. Launch:**
*   Open the `w64devkit` terminal.
*   Navigate to the game folder: `cd path/to/RootBound`
*   Type `make` and press Enter.
*   Run the game: `./rootbound.exe`

---

## 🛠 For the Developers (The Technical Version)

### Technical Architecture
The project is implemented in **C99** and utilizes **Raylib** for hardware-accelerated 2D rendering. 

**Key Technical Features:**
*   **Manual Memory Management:** No garbage collector. All game entities and assets are allocated and freed manually to prevent memory leaks and ensure a constant frame rate.
*   **Game Loop:** Implements a standard `Update -> Draw` loop. 
    *   `Update()`: Handles input polling, collision detection, and state changes.
    *   `Draw()`: Handles texture rendering and UI layering.
*   **Struct-Based Entity System:** Uses C structs to define player and world properties, ensuring data is contiguous in memory for better CPU cache performance.
*   **Modular Design:** The logic is split into separate `.c` and `.h` files (header files) to keep the codebase maintainable and scalable.

### Build System
The project uses a **Makefile**. The Makefile automates the GCC compilation process, linking the `raylib` library and specifying the necessary flags (like `-Wall` for warnings and `-O3` for optimization).

### Directory Structure
- `/src`: Contains all the source code (`.c` files).
- `/include`: Contains the header files (`.h`) defining the game's API.
- `/assets`: Contains textures, sounds, and fonts.
- `Makefile`: The build script for compiling the game.

---

## ⚠️ Known Issues & Troubleshooting
*(We will be filling this section tomorrow as we squash bugs!)*

- **Linker Errors:** Usually caused by Raylib not being in the correct search path.
- **Black Screen:** Usually caused by missing asset files in the `/assets` folder.
- **Crash on Start:** Check if the GPU drivers support OpenGL 3.3.
