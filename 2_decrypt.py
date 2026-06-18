import json
from hardware import HardwareSRAM
from transformer import DataTransformer

def decrypt_dataset():
    hw = HardwareSRAM()
    transformer = DataTransformer()

    print("Step 1: Loading 'weird' sequences from database.json...")
    try:
        with open("database.json", "r") as f:
            stored_data = json.load(f)
    except FileNotFoundError:
        print("Error: database.json not found. Please run 1_encrypt.py first.")
        return

    print("Step 2: Querying hardware for ephemeral Part B...")

    reconstructed_dataset = []
    for row in stored_data:
        # Derive Part B fresh for each record to ensure it's not sitting in RAM
        temp_b = bytearray(hw.derive_part_b())

        reconstructed_row = {}
        for key, value in row.items():
            # Reconstruct using the fresh Part B
            reconstructed_row[key] = transformer.reconstruct(value, temp_b)

        reconstructed_dataset.append(reconstructed_row)

        # Simulate the 25ms RAM window then wipe
        hw.wipe_memory(temp_b)
        del temp_b

    print("\nSUCCESS: Data Reconstructed from Hardware Secret!")
    print("-" * 40)
    for row in reconstructed_dataset:
        print(row)
    print("-" * 40)

if __name__ == "__main__":
    decrypt_dataset()
