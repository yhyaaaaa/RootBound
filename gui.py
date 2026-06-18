import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from hardware import HardwareSRAM
from transformer import DataTransformer

class SecurityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum-Hardware Data Vault")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e1e")

        self.hw = HardwareSRAM()
        self.transformer = DataTransformer()
        self.db_path = "database.json"

        # Styling
        style = ttk.Style()
        style.theme_use('clam')

        # Main Frame
        main_frame = tk.Frame(root, bg="#1e1e1e", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input Section ---
        input_group = tk.LabelFrame(main_frame, text=" Enter Data to Secure ", fg="white", bg="#1e1e1e", padx=10, pady=10)
        input_group.pack(fill=tk.X, pady=10)

        tk.Label(input_group, text="Name:", fg="#aaa", bg="#1e1e1e").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_name = tk.Entry(input_group, width=40)
        self.ent_name.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(input_group, text="Phone:", fg="#aaa", bg="#1e1e1e").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_phone = tk.Entry(input_group, width=40)
        self.ent_phone.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(input_group, text="ID:", fg="#aaa", bg="#1e1e1e").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_id = tk.Entry(input_group, width=40)
        self.ent_id.grid(row=2, column=1, pady=5, padx=10)

        self.btn_store = tk.Button(input_group, text="Store Securely", command=self.store_data,
                                   bg="#007acc", fg="white", relief="flat", padx=10, pady=5)
        self.btn_store.grid(row=3, column=1, sticky="e", pady=10)

        # --- Database View (Part A) ---
        db_group = tk.LabelFrame(main_frame, text=" Database View (Part A - Stored) ", fg="white", bg="#1e1e1e", padx=10, pady=10)
        db_group.pack(fill=tk.BOTH, expand=True, pady=10)

        self.txt_db = tk.Text(db_group, height=10, bg="#2d2d2d", fg="#88ff88", font=("Courier New", 10))
        self.txt_db.pack(fill=tk.BOTH, expand=True)

        self.btn_refresh_db = tk.Button(db_group, text="Refresh DB View", command=self.refresh_db_view,
                                      bg="#444", fg="white", relief="flat")
        self.btn_refresh_db.pack(pady=5)

        # --- Reconstruction View ---
        rec_group = tk.LabelFrame(main_frame, text=" Reconstructed View (Authorized Query) ", fg="white", bg="#1e1e1e", padx=10, pady=10)
        rec_group.pack(fill=tk.BOTH, expand=True, pady=10)

        # Move the button ABOVE the text box so it's always visible
        self.btn_reconstruct = tk.Button(rec_group, text="Query Hardware & Reconstruct", command=self.reconstruct_data,
                                        bg="#d95319", fg="white", relief="flat", padx=10, pady=5)
        self.btn_reconstruct.pack(pady=(0, 10))

        self.txt_rec = tk.Text(rec_group, height=8, bg="#2d2d2d", fg="#ffffff", font=("Courier New", 10))
        self.txt_rec.pack(fill=tk.BOTH, expand=True)

        # Initial load
        self.refresh_db_view()

    def store_data(self):
        name = self.ent_name.get()
        phone = self.ent_phone.get()
        uid = self.ent_id.get()

        if not (name and phone and uid):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        # Deriving Part B
        part_b = bytearray(self.hw.derive_part_b())

        # Transforming data
        new_row = {
            "name": self.transformer.transform(name, part_b),
            "phone": self.transformer.transform(phone, part_b),
            "id": self.transformer.transform(uid, part_b)
        }

        # Wipe Part B from memory immediately
        self.hw.wipe_memory(part_b)

        # Load and append to database
        data = []
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                data = json.load(f)

        data.append(new_row)

        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=4)

        # Clear inputs and refresh
        self.ent_name.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)
        self.ent_id.delete(0, tk.END)
        self.refresh_db_view()
        messagebox.showinfo("Success", "Data secured and Part B wiped from RAM!")

    def refresh_db_view(self):
        self.txt_db.delete("1.0", tk.END)
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                data = json.load(f)
                self.txt_db.insert(tk.END, json.dumps(data, indent=4))
        else:
            self.txt_db.insert(tk.END, "Database empty.")

    def reconstruct_data(self):
        if not os.path.exists(self.db_path):
            messagebox.showerror("Error", "No data to reconstruct.")
            return

        with open(self.db_path, "r") as f:
            stored_data = json.load(f)

        self.txt_rec.delete("1.0", tk.END)

        try:
            for row in stored_data:
                # Derive Part B fresh for each query
                temp_b = bytearray(self.hw.derive_part_b())

                reconstructed_row = {}
                for key, value in row.items():
                    reconstructed_row[key] = self.transformer.reconstruct(value, temp_b)

                # Wipe RAM window
                self.hw.wipe_memory(temp_b)

                self.txt_rec.insert(tk.END, f"{reconstructed_row}\n")
        except Exception as e:
            self.txt_rec.insert(tk.END, f"Error during reconstruction: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityGUI(root)
    root.mainloop()
