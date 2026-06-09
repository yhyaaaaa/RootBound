import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import hashlib
import sqlite3
from hardware import HardwareSRAM
from transformer import DataTransformer
from database_manager import DatabaseManager

class AdminPanel(tk.Toplevel):
    """
    A popup window for managing users and their access.
    Restricted to root:root access.
    """
    def __init__(self, parent):
        super().__init__()
        self.db = DatabaseManager()
        self.title("RootBound - Admin Management")
        self.geometry("500x400")
        self.configure(bg="#1e1e1e")

        main_frame = tk.Frame(self, bg="#1e1e1e", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="USER MANAGEMENT", fg="#d95319", bg="#1e1e1e",
                 font=("Courier New", 14, "bold")).pack(pady=(0, 20))

        self.user_listbox = tk.Listbox(main_frame, bg="#2d2d2d", fg="white",
                                       font=("Courier New", 10), selectbackground="#007acc")
        self.user_listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        btn_frame = tk.Frame(main_frame, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Refresh List", command=self.refresh_users,
                  bg="#444", fg="white", relief="flat", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete User", command=self.delete_user,
                  bg="#a30000", fg="white", relief="flat", width=15).pack(side=tk.LEFT, padx=5)

        self.refresh_users()

    def refresh_users(self):
        self.user_listbox.delete(0, tk.END)
        with sqlite3.connect("vault.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users")
            for row in cursor.fetchall():
                self.user_listbox.insert(tk.END, row[0])

    def delete_user(self):
        selected = self.user_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a user to delete.")
            return

        username = self.user_listbox.get(selected[0])
        if username == "root":
            messagebox.showerror("Error", "Cannot delete the root administrator!")
            return

        with sqlite3.connect("vault.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()

        messagebox.showinfo("Success", f"User {username} has been removed.")
        self.refresh_users()

class LoginFrame(tk.Frame):
    """
    Authentication frame that lives inside the root window.
    """
    def __init__(self, parent, on_success):
        super().__init__(parent, bg="#1e1e1e")
        self.on_success = on_success
        self.hw = HardwareSRAM()
        self.db = DatabaseManager()

        main_frame = tk.Frame(self, bg="#1e1e1e", padx=20, pady=30)
        main_frame.pack(expand=True)

        tk.Label(main_frame, text="ROOTBOUND VAULT", fg="#007acc", bg="#1e1e1e",
                 font=("Courier New", 18, "bold")).pack(pady=(0, 20))

        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()

        tk.Label(main_frame, text="Username", fg="#aaa", bg="#1e1e1e").pack()
        tk.Entry(main_frame, textvariable=self.user_var, width=30).pack(pady=5)

        tk.Label(main_frame, text="Password", fg="#aaa", bg="#1e1e1e").pack()
        tk.Entry(main_frame, textvariable=self.pass_var, width=30, show="*").pack(pady=5)

        btn_frame = tk.Frame(main_frame, bg="#1e1e1e")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Login", command=self.login,
                  bg="#007acc", fg="white", relief="flat", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Register", command=self.register,
                  bg="#444", fg="white", relief="flat", width=10).pack(side=tk.LEFT, padx=5)

    def get_hw_bound_hash(self, password):
        hw_id = self.hw._get_hw_ids()
        combined = f"{password}{hw_id}".encode()
        return hashlib.sha256(combined).hexdigest()

    def login(self):
        username = self.user_var.get()
        password = self.pass_var.get()

        if not username or not password:
            messagebox.showwarning("Login Error", "Please enter both username and password.")
            return

        password_hash = self.get_hw_bound_hash(password)
        if self.db.verify_user(username, password_hash):
            messagebox.showinfo("Success", "Hardware Verified. Access Granted.")
            self.on_success()
        else:
            messagebox.showerror("Access Denied", "Invalid credentials or unauthorized hardware.")

    def register(self):
        username = self.user_var.get()
        password = self.pass_var.get()

        if not username or not password:
            messagebox.showwarning("Register Error", "Please enter both username and password.")
            return

        password_hash = self.get_hw_bound_hash(password)
        if self.db.create_user(username, password_hash):
            messagebox.showinfo("Success", "Account created and bound to this hardware!")
        else:
            messagebox.showerror("Error", "Username already exists.")

class SecurityGUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")
        self.root = parent.master # Link back to root for Toplevels
        self.hw = HardwareSRAM()
        self.transformer = DataTransformer()
        self.db = DatabaseManager()

        # Styling
        style = ttk.Style()
        style.theme_use('clam')

        main_frame = tk.Frame(self, bg="#1e1e1e", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.btn_admin = tk.Button(main_frame, text="Admin Access", command=self.open_admin_login,
                                  bg="#333", fg="#aaa", relief="flat", padx=10)
        self.btn_admin.pack(anchor="ne", pady=(0, 10))

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

        db_group = tk.LabelFrame(main_frame, text=" Database View (Part A - Stored) ", fg="white", bg="#1e1e1e", padx=10, pady=10)
        db_group.pack(fill=tk.BOTH, expand=True, pady=10)

        self.txt_db = tk.Text(db_group, height=10, bg="#2d2d2d", fg="#88ff88", font=("Courier New", 10))
        self.txt_db.pack(fill=tk.BOTH, expand=True)

        self.btn_refresh_db = tk.Button(db_group, text="Refresh DB View", command=self.refresh_db_view,
                                      bg="#444", fg="white", relief="flat")
        self.btn_refresh_db.pack(pady=5)

        rec_group = tk.LabelFrame(main_frame, text=" Reconstructed View (Authorized Query) ", fg="white", bg="#1e1e1e", padx=10, pady=10)
        rec_group.pack(fill=tk.BOTH, expand=True, pady=10)

        self.btn_reconstruct = tk.Button(rec_group, text="Query Hardware & Reconstruct", command=self.reconstruct_data,
                                        bg="#d95319", fg="white", relief="flat", padx=10, pady=5)
        self.btn_reconstruct.pack(pady=(0, 10))

        self.txt_rec = tk.Text(rec_group, height=8, bg="#2d2d2d", fg="#ffffff", font=("Courier New", 10))
        self.txt_rec.pack(fill=tk.BOTH, expand=True)

        self.refresh_db_view()

    def open_admin_login(self):
        auth_win = tk.Toplevel(self.root)
        auth_win.title("Admin Auth")
        auth_win.geometry("300x150")
        auth_win.configure(bg="#1e1e1e")

        tk.Label(auth_win, text="Enter Admin Password", fg="white", bg="#1e1e1e").pack(pady=10)
        pass_ent = tk.Entry(auth_win, show="*")
        pass_ent.pack(pady=5)

        def check():
            if pass_ent.get() == "root":
                auth_win.destroy()
                AdminPanel(self.root)
            else:
                messagebox.showerror("Denied", "Incorrect Admin Password")

        tk.Button(auth_win, text="Unlock", command=check, bg="#d95319", fg="white", relief="flat").pack(pady=10)

    def store_data(self):
        name = self.ent_name.get()
        phone = self.ent_phone.get()
        uid = self.ent_id.get()

        if not (name and phone and uid):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        part_b = bytearray(self.hw.derive_part_b())
        transformed_name = self.transformer.transform(name, part_b)
        transformed_phone = self.transformer.transform(phone, part_b)
        transformed_id = self.transformer.transform(uid, part_b)
        self.hw.wipe_memory(part_b)
        self.db.store_record(transformed_name, transformed_phone, transformed_id)
        self.ent_name.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)
        self.ent_id.delete(0, tk.END)
        self.refresh_db_view()
        messagebox.showinfo("Success", "Data secured and Part B wiped from RAM!")

    def refresh_db_view(self):
        self.txt_db.delete("1.0", tk.END)
        records = self.db.get_all_records()
        if records:
            for row in records:
                self.txt_db.insert(tk.END, f"Name: {row[0]}\nPhone: {row[1]}\nID: {row[2]}\n{'-'*30}\n")
        else:
            self.txt_db.insert(tk.END, "Database empty.")

    def reconstruct_data(self):
        records = self.db.get_all_records()
        if not records:
            messagebox.showerror("Error", "No data to reconstruct.")
            return
        self.txt_rec.delete("1.0", tk.END)
        try:
            for row in records:
                temp_b = bytearray(self.hw.derive_part_b())
                reconstructed_name = self.transformer.reconstruct(row[0], temp_b)
                reconstructed_phone = self.transformer.reconstruct(row[1], temp_b)
                reconstructed_id = self.transformer.reconstruct(row[2], temp_b)
                self.hw.wipe_memory(temp_b)
                self.txt_rec.insert(tk.END, f"Name: {reconstructed_name}, Phone: {reconstructed_phone}, ID: {reconstructed_id}\n")
        except Exception as e:
            self.txt_rec.insert(tk.END, f"Error during reconstruction: {e}")

def main():
    root = tk.Tk()
    root.title("RootBound")
    root.geometry("600x750")
    root.configure(bg="#1e1e1e")

    current_frame = None

    def show_vault():
        nonlocal current_frame
        if current_frame:
            current_frame.pack_forget() # Hide the login frame
            current_frame.destroy()
        current_frame = SecurityGUI(root)
        current_frame.pack(fill=tk.BOTH, expand=True)

    def show_login():
        nonlocal current_frame
        if current_frame:
            current_frame.destroy()
        current_frame = LoginFrame(root, on_success=show_vault)
        current_frame.pack(fill=tk.BOTH, expand=True)

    show_login()
    root.mainloop()

if __name__ == "__main__":
    main()
