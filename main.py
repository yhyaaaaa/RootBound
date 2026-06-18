import time
from hardware import HardwareSRAM
from transformer import DataTransformer

def run_demo():
    print("=== Data Security System Demo (SRAM-PUF Derived) ===")

    # 1. Setup simulated hardware and dataset
    hw = HardwareSRAM()
    transformer = DataTransformer()

    dataset = [
        {"name": "Alice Smith", "phone": "555-0101", "id": "S123"},
        {"name": "Bob Jones", "phone": "555-0202", "id": "S456"},
        {"name": "Charlie Brown", "phone": "555-0303", "id": "S789"},
    ]

    print("\n[Step 1] Original Dataset:")
    for row in dataset:
        print(f"  {row}")

    # 2. Transformation Phase
    print("\n[Step 2] Transformation Process...")
    # In this phase, we derive Part B once to encrypt the dataset
    part_b = bytearray(hw.derive_part_b())

    stored_data = []
    for row in dataset:
        transformed_row = {}
        for key, value in row.items():
            # Transform each value into a 'weird sequence' (Part A)
            transformed_row[key] = transformer.transform(value, part_b)
        stored_data.append(transformed_row)

    # IMMEDIATELY wipe Part B from memory as per requirement
    hw.wipe_memory(part_b)
    del part_b

    print("\n[Step 3] Stored Dataset (Part A only):")
    print("Notice: Part B is NOT stored. If you steal this, it's useless.")
    for row in stored_data:
        print(f"  {row}")

    # 3. Reconstruction Phase
    print("\n[Step 4] Reconstructing Data...")
    print("Querying hardware for ephemeral Part B...")

    reconstructed_dataset = []
    for row in stored_data:
        # For every record, we derive Part B fresh
        temp_b = bytearray(hw.derive_part_b())

        reconstructed_row = {}
        for key, value in row.items():
            # Reconstruct using the fresh Part B
            reconstructed_row[key] = transformer.reconstruct(value, temp_b)

        reconstructed_dataset.append(reconstructed_row)

        # Simulate the 25ms RAM window then wipe
        time.sleep(0.025)
        hw.wipe_memory(temp_b)
        del temp_b

    print("\n[Step 5] Reconstructed Dataset:")
    for row in reconstructed_dataset:
        print(f"  {row}")

    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    run_demo()
