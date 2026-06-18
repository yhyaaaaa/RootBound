# RootBound 🔐

A high-security data storage system that utilizes physical hardware characteristics as a root of trust. This project implements a "Split Secret" architecture where data is fragmented into a stored part (Part A) and a hardware-derived part (Part B).

## 🚀 Overview
The system ensures that data is not just encrypted, but **physically bound** to a specific piece of hardware. Even if the entire database is stolen, the data remains useless without the original physical server's silicon.

### The Core Concept: Part A & Part B
- **Part A (Stored):** The transformed "weird sequences" stored in a SQL database.
- **Part B (Ephemeral):** A secret key derived on-the-fly from the server's hardware identifiers. It is **never stored on disk**.

---

## 🛠️ Technical Specifications

### 1. Hardware Derivation (SRAM PUF Simulation)
The system derives Part B by scanning the physical hardware of the machine:
- **Inputs:** Motherboard UUID and CPU Processor ID.
- **Method:** These identifiers are combined and passed through a **SHA-256** cryptographic hash.
- **Result:** A unique, deterministic 32-byte key that is specific to that individual motherboard/CPU combination.

### 2. Data Transformation Logic
To transform normal data into Part A:
- **XOR Stream Cipher:** The plaintext is XORed with the derived Part B.
- **Base64 Encoding:** The resulting binary is encoded into Base64 strings, creating the "weird" look of the stored data.
- **Reversibility:** Because XOR is symmetric, applying Part B a second time perfectly reconstructs the original data.

### 3. Ephemeral RAM Management
To prevent memory dump attacks (Cold Boot attacks), the system implements a strict memory lifecycle:
- Part B is generated only during a query.
- After use, the system performs a **manual byte-wipe**, overwriting the `bytearray` with zeros before deleting the reference.
- This ensures the secret exists in RAM for only a few milliseconds.

---

## 💻 How to Use

### Prerequisites
- Python 3.x
- (Optional) Docker for server deployment

### Running the CLI Demo
1. **Store Data:**
   ```bash
   python 1_encrypt.py
   ```
   *This generates the `vault.db` SQL database with encrypted records.*

2. **Inspect the Database:**
   Open `vault.db` with any SQLite viewer to see the "weird sequences."

3. **Reconstruct Data:**
   ```bash
   python 2_decrypt.py
   ```

### Running the GUI
For a full visual demonstration:
```bash
python gui.py
```

### Docker Deployment
To run this on a production server, you must allow the container to access the physical hardware IDs:
```bash
docker build -t security-puf-demo .
docker run --privileged -v /sys:/sys security-puf-demo
```

---

## 🛡️ Security Analysis
- **Database Theft:** ❌ Impossible to decrypt without the specific physical server.
- **Cloning/VM Migration:** ❌ Fails; the new environment will have different hardware IDs, resulting in a different Part B.
- **Root Access:** ⚠️ Partial risk; however, the a-temporal nature of the RAM wipe limits the window of attack.
- **Hardware Bound:** ✅ The secret is an emergent property of the hardware, not a stored file.
