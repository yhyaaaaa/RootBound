import json
from hardware import HardwareSRAM
from transformer import DataTransformer

def encrypt_dataset():
    hw = HardwareSRAM()
    transformer = DataTransformer()

    # Normal looking input
    dataset = [
        {"name": "Alice Smith", "phone": "555-0101", "id": "S123"},
        {"name": "Bob Jones", "phone": "555-0202", "id": "S456"},
        {"name": "Charlie Brown", "phone": "555-0303", "id": "S789"},
    ]

    print("Step 1: Deriving hardware secret (Part B)...")
    part_b = bytearray(hw.derive_part_b())

    print("Step 2: Transforming data into 'weird sequences' (Part A)...")
    stored_data = []
    for row in dataset:
        transformed_row = {}
        for key, value in row.items():
            transformed_row[key] = transformer.transform(value, part_b)
        stored_data.append(transformed_row)

    # Wipe the secret from RAM
    hw.wipe_memory(part_b)

    # Store ONLY Part A in the "database"
    with open("database.json", "w") as f:
        json.dump(stored_data, f, indent=4)

    print("\nSUCCESS: Data has been transformed and saved to database.json")
    print("Part B has been wiped from memory.")

if __name__ == "__main__":
    encrypt_dataset()
