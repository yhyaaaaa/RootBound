import hashlib
from transformer import DataTransformer

def simulate_attack(stored_data, attacker_hw_id):
    """
    Simulates an attacker who has stolen the 'weird' sequences (Part A)
    and is trying to decrypt them using a different hardware ID.
    """
    print("\n--- ATTACK SIMULATION START ---")
    print(f"Attacker has stolen the data and is using Hardware ID: {attacker_hw_id}")

    # Attacker derives their own Part B from THEIR hardware
    attacker_part_b = hashlib.sha256(attacker_hw_id.encode()).digest()
    transformer = DataTransformer()

    print("\nAttempting to decrypt first record...")
    first_row = stored_data[0]

    try:
        # Attempt to reconstruct 'name' using the wrong Part B
        decrypted_name = transformer.reconstruct(first_row['name'], attacker_part_b)
        print(f"Result: {decrypted_name}")
        print("\nCRITICAL FAILURE: Data was decrypted using wrong hardware!")
    except Exception as e:
        print(f"Result: [GARBAGE DATA / ERROR]")
        print("\nSUCCESS: The data remains encrypted because the hardware IDs do not match.")

    print("--- ATTACK SIMULATION END ---\n")

if __name__ == "__main__":
    # This is what 'Part A' looks like in your database
    mock_stored_data = [
        {'name': '7+CiEq9uEKb4aA8=', 'phone': 'm7n+XPp/c/o=', 'id': '/b35Qg=='}
    ]

    # The attacker is on a different machine
    attacker_id = "HACKER-PC-SRAM-99999"

    simulate_attack(mock_stored_data, attacker_id)
