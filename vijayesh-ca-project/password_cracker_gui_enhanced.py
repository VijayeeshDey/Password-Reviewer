# Password Security Analysis - Enhanced GUI Version
# CA Project - Cyber Security
# Run: python password_cracker_gui_enhanced.py

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import time

# Pre-set breach hashes to practice with
BREACH_HASHES = {
    "e10adc3949ba59abbe56e057f20f883e": "123456",
    "5f4dcc3b5aa765d61d8327deb882cf99": "password",
    "827ccb0eea8a706c4c34a16891f84e7b": "12345",
    "202cb962ac59075b964b07152d234b70": "123",
    "098f6bcd4621d373cade4e832627b4f6": "test",
    "5d41402abc4b2a76b9719d911017c592": "hello",
    "0d107d09f5bbe40cade3de5c71e9e9b7": "letmein",
    "d8578edf8458ce06fbc5bb76a58c5ca4": "qwerty",
    "96e79218955eb5b7a9342158a4190386": "123456789",
    "25f9e794323b453885f5181f1b624d0b": "1234567890",
}

class PasswordCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Security Analysis - CA Project")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1a1a2e")

        self.current_hash = None
        self.attempt_count = 0
        self.start_time = None

        self.setup_ui()

    def setup_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="POST-BREACH PASSWORD SECURITY ANALYSIS",
            font=("Arial", 20, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            self.root,
            text="Learn how passwords are cracked | MD5 Vulnerability Demo",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#888"
        )
        subtitle.pack(pady=2)

        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # LEFT PANEL - Controls
        left_frame = tk.Frame(main_frame, bg="#1a1a2e")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Step 1: Select Hash
        tk.Label(left_frame, text="STEP 1: Select a Hash to Crack",
                 font=("Arial", 12, "bold"), bg="#1a1a2e", fg="#ff6b6b").pack(pady=10)

        tk.Label(left_frame, text="Choose a hash from practice list:",
                 bg="#1a1a2e", fg="white").pack()

        # Hash selection buttons
        hash_frame = tk.Frame(left_frame, bg="#1a1a2e")
        hash_frame.pack(pady=5)

        i = 0
        for h, p in list(BREACH_HASHES.items())[:5]:
            btn = tk.Button(
                hash_frame,
                text=f"Hash {i+1}",
                font=("Arial", 9),
                bg="#4a4a6a",
                fg="white",
                command=lambda h=h: self.select_hash(h),
                width=10
            )
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            i += 1

        # Display selected hash
        tk.Label(left_frame, text="Selected Hash:", bg="#1a1a2e", fg="white").pack(pady=10)
        self.selected_hash_label = tk.Label(
            left_frame,
            text="No hash selected",
            font=("Courier", 10),
            bg="#0f0f23",
            fg="#00ff00",
            width=40,
            height=2,
            wraplength=350
        )
        self.selected_hash_label.pack(pady=5)

        # Step 2: Try Password
        tk.Label(left_frame, text="STEP 2: Try to Crack It",
                 font=("Arial", 12, "bold"), bg="#1a1a2e", fg="#ff6b6b").pack(pady=10)

        tk.Label(left_frame, text="Enter a password to try:",
                 bg="#1a1a2e", fg="white").pack()

        self.password_entry = tk.Entry(left_frame, font=("Arial", 12), width=25)
        self.password_entry.pack(pady=5)

        # Try button
        try_btn = tk.Button(
            left_frame,
            text="TRY PASSWORD",
            font=("Arial", 11, "bold"),
            bg="#e94560",
            fg="white",
            command=self.try_password,
            width=18
        )
        try_btn.pack(pady=5)

        # Auto-crack button
        auto_btn = tk.Button(
            left_frame,
            text="AUTO-CRACK (Dictionary)",
            font=("Arial", 11, "bold"),
            bg="#4a4a6a",
            fg="white",
            command=self.auto_crack,
            width=20
        )
        auto_btn.pack(pady=10)

        # Brute force button
        brute_btn = tk.Button(
            left_frame,
            text="BRUTE FORCE (Slow)",
            font=("Arial", 11, "bold"),
            bg="#4a4a6a",
            fg="white",
            command=self.brute_force,
            width=20
        )
        brute_btn.pack(pady=5)

        # Result display
        tk.Label(left_frame, text="RESULT:", bg="#1a1a2e", fg="white").pack(pady=10)
        self.result_label = tk.Label(
            left_frame,
            text="Not cracked yet",
            font=("Arial", 14, "bold"),
            bg="#0f0f23",
            fg="#888",
            width=30,
            height=3
        )
        self.result_label.pack(pady=5)

        # RIGHT PANEL - Stats & History
        right_frame = tk.Frame(main_frame, bg="#1a1a2e")
        right_frame.pack(side="right", fill="both", expand=True, padx=5)

        # Stats
        stats_frame = tk.Frame(right_frame, bg="#16213e")
        stats_frame.pack(fill="x", pady=5)

        tk.Label(stats_frame, text="ATTEMPTS & STATS",
                 font=("Arial", 12, "bold"), bg="#16213e", fg="#00d4ff").pack(pady=5)

        self.attempts_label = tk.Label(stats_frame, text="Attempts: 0",
                                        font=("Arial", 11), bg="#16213e", fg="white")
        self.attempts_label.pack(pady=2)

        self.time_label = tk.Label(stats_frame, text="Time: 0.000s",
                                    font=("Arial", 11), bg="#16213e", fg="white")
        self.time_label.pack(pady=2)

        self.status_label = tk.Label(stats_frame, text="Status: Ready",
                                      font=("Arial", 11), bg="#16213e", fg="#ff6b6b")
        self.status_label.pack(pady=2)

        # Attempt history
        tk.Label(right_frame, text="ATTEMPT HISTORY",
                 font=("Arial", 12, "bold"), bg="#1a1a2e", fg="#00d4ff").pack(pady=10)

        self.history_tree = ttk.Treeview(right_frame, columns=("#", "Password", "Hash Match"), height=10, show="headings")
        self.history_tree.heading("#", text="#")
        self.history_tree.heading("Password", text="Password Tried")
        self.history_tree.heading("Hash Match", text="Result")

        self.history_tree.column("#", width=40)
        self.history_tree.column("Password", width=150)
        self.history_tree.column("Hash Match", width=100)

        self.history_tree.pack(fill="both", expand=True)

        # Common passwords hint
        hint_frame = tk.Frame(right_frame, bg="#16213e")
        hint_frame.pack(fill="x", pady=10)

        tk.Label(hint_frame, text="Try these common passwords:",
                 font=("Arial", 10), bg="#16213e", fg="white").pack()

        hint_text = "123456, password, 12345, test, hello, qwerty, letmein, 123, admin, 123456789"
        tk.Label(hint_frame, text=hint_text, font=("Courier", 8),
                 bg="#16213e", fg="#888", wraplength=300).pack(pady=5)

        # Bottom panel - Risk level
        risk_frame = tk.Frame(self.root, bg="#0f0f23", height=50)
        risk_frame.pack(fill="x", side="bottom")

        self.risk_label = tk.Label(
            risk_frame,
            text="SECURITY RISK: NOT ASSESSED",
            font=("Arial", 14, "bold"),
            bg="#0f0f23",
            fg="#888"
        )
        self.risk_label.pack(pady=10)

    def select_hash(self, hash_val):
        self.current_hash = hash_val
        self.selected_hash_label.config(
            text=f"Hash: {hash_val[:30]}...",
            fg="#00ff00"
        )
        self.result_label.config(text="Not cracked yet", fg="#888")
        self.status_label.config(text="Status: Hash selected - try passwords!", fg="#00d4ff")
        self.attempts_label.config(text="Attempts: 0")
        self.risk_label.config(text="SECURITY RISK: NOT ASSESSED", fg="#888")

        # Clear history
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        self.attempt_count = 0
        self.start_time = None

    def try_password(self):
        if not self.current_hash:
            messagebox.showwarning("No Hash", "Please select a hash first!")
            return

        password = self.password_entry.get().strip()

        if not password:
            messagebox.showwarning("No Input", "Enter a password to try!")
            return

        self.attempt_count += 1
        if not self.start_time:
            self.start_time = time.time()

        # Compute hash of input
        input_hash = hashlib.md5(password.encode()).hexdigest()

        # Add to history
        if input_hash == self.current_hash:
            self.history_tree.insert("", "end", values=(self.attempt_count, password, "MATCH!"))
            self.result_label.config(text=f"✓ CRACKED: {password}", fg="#00ff00")
            self.status_label.config(text="Status: SUCCESS!", fg="#00ff00")
            self.risk_label.config(text="SECURITY RISK: CRITICAL - All passwords can be cracked!", fg="#ff0000")
            elapsed = time.time() - self.start_time
            self.time_label.config(text=f"Time: {elapsed:.3f}s")
            messagebox.showinfo("SUCCESS!", f"Password cracked: {password}\nAttempts: {self.attempt_count}")
        else:
            self.history_tree.insert("", "end", values=(self.attempt_count, password, "Wrong"))
            self.result_label.config(text="Not correct - try again!", fg="#ff6b6b")
            self.status_label.config(text=f"Status: {self.attempt_count} attempts failed", fg="#ff6b6b")
            elapsed = time.time() - self.start_time if self.start_time else 0
            self.time_label.config(text=f"Time: {elapsed:.3f}s")
            self.attempts_label.config(text=f"Attempts: {self.attempt_count}")

        self.password_entry.delete(0, tk.END)

    def auto_crack(self):
        if not self.current_hash:
            messagebox.showwarning("No Hash", "Please select a hash first!")
            return

        wordlist = [
            '123456', 'password', '12345', '123', 'test', 'hello',
            'qwerty', 'letmein', '123456789', '12345678', 'admin',
            'welcome', 'monkey', 'dragon', 'master', 'pass', 'sunshine',
            'princess', 'football', '1234567890', 'baseball', 'iloveyou',
            'trustno1', 'shadow', 'ashley', 'michael', 'superman', '666666',
            '7777777', '888888', 'password1', 'password123', 'letmein123'
        ]

        self.status_label.config(text="Status: Cracking...", fg="#00d4ff")
        self.root.update()

        start = time.time()
        found = False

        for i, pwd in enumerate(wordlist):
            computed = hashlib.md5(pwd.encode()).hexdigest()

            self.history_tree.insert("", "end", values=(i+1, pwd, "Trying..."))
            self.root.update()

            if computed == self.current_hash:
                elapsed = time.time() - start
                self.result_label.config(text=f"✓ CRACKED: {pwd}", fg="#00ff00")
                self.status_label.config(text="Status: SUCCESS!", fg="#00ff00")
                self.risk_label.config(text="SECURITY RISK: CRITICAL", fg="#ff0000")
                self.attempts_label.config(text=f"Attempts: {i+1}")
                self.time_label.config(text=f"Time: {elapsed:.4f}s")
                self.attempt_count = i + 1
                found = True

                messagebox.showinfo("CRACKED!", f"Password found: {pwd}\nAttempts: {i+1}\nTime: {elapsed:.4f}s")
                break

        if not found:
            self.result_label.config(text="Not in wordlist", fg="#ff6b6b")
            self.status_label.config(text="Status: Failed", fg="#ff6b6b")

    def brute_force(self):
        if not self.current_hash:
            messagebox.showwarning("No Hash", "Please select a hash first!")
            return

        # Only do numeric brute force for demo (1-4 digits)
        import itertools

        self.status_label.config(text="Status: Brute forcing...", fg="#00d4ff")
        self.root.update()

        start = time.time()

        for length in range(1, 5):
            for combo in itertools.product('0123456789', repeat=length):
                pwd = ''.join(combo)
                computed = hashlib.md5(pwd.encode()).hexdigest()

                self.attempt_count += 1

                if self.attempt_count % 100 == 0:
                    self.attempts_label.config(text=f"Attempts: {self.attempt_count}")
                    self.root.update()

                if computed == self.current_hash:
                    elapsed = time.time() - start
                    self.result_label.config(text=f"✓ CRACKED: {pwd}", fg="#00ff00")
                    self.status_label.config(text="Status: SUCCESS!", fg="#00ff00")
                    self.time_label.config(text=f"Time: {elapsed:.2f}s")
                    messagebox.showinfo("CRACKED!", f"Password found: {pwd}\nAttempts: {self.attempt_count}")
                    return

        self.result_label.config(text="Brute force limited", fg="#ff6b6b")
        messagebox.showinfo("Note", "Brute force is slow!\nFor better results, use dictionary attack or try common passwords manually.")


def main():
    root = tk.Tk()
    app = PasswordCrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()