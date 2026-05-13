# Password Security Analysis - GUI Version
# CA Project - Cyber Security
# Run: python password_cracker_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import threading
import time
try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    print("Note: pygame not installed. Audio features will be limited.")

import os

# Audio files from desktop
AUDIO_PATH = r"C:\Users\mohak\OneDrive\Desktop"
AUDIO_START = os.path.join(AUDIO_PATH, "Urdta hi firu.mp3")      # 1st audio - plays during 32s
AUDIO_CRACKED = os.path.join(AUDIO_PATH, "Lau ne Bhojyam.mp3")   # 2nd audio - when cracked
AUDIO_NOT_CRACKED = os.path.join(AUDIO_PATH, "Wah modi.mp3")     # 3rd audio - when not cracked

# Simulated breach data - 20 password hashes with answers
BREACH_DATA = [
    ("e10adc3949ba59abbe56e057f20f883e", "john.doe", "123456"),
    ("5f4dcc3b5aa765d61d8327deb882cf99", "admin", "password"),
    ("827ccb0eea8a706c4c34a16891f84e7b", "sarah.smith", "12345"),
    ("202cb962ac59075b964b07152d234b70", "mike.wilson", "123"),
    ("098f6bcd4621d373cade4e832627b4f6", "emily.brown", "test"),
    ("5d41402abc4b2a76b9719d911017c592", "david.lee", "hello"),
    ("0d107d09f5bbe40cade3de5c71e9e9b7", "user16", "letmein"),
    ("96e79218955eb5b7a9342158a4190386", "user11", "123456789"),
    ("25f9e794323b453885f5181f1b624d0b", "user12", "1234567890"),
    ("d8578edf8458ce06fbc5bb76a58c5ca4", "test_user", "qwerty"),
    ("098f6bcd4621d373cade4e832627b4f6", "user19", "test"),
    ("202cb962ac59075b964b07152d234b70", "user14", "123"),
    ("e10adc3949ba59abbe56e057f20f883e", "chris.martin", "123456"),
    ("5f4dcc3b5aa765d61d8327deb882cf99", "admin2", "password"),
    ("827ccb0eea8a706c4c34a16891f84e7b", "user13", "12345"),
    ("5d41402abc4b2a76b9719d911017c592", "user15", "hello"),
    ("d8578edf8458ce06fbc5bb76a58c5ca4", "keyboard_user", "qwerty"),
    ("0d107d09f5bbe40cade3de5c71e9e9b7", "user17", "letmein"),
    ("96e79218955eb5b7a9342158a4190386", "user18", "123456789"),
    ("5f4dcc3b5aa765d61d8327deb882cf99", "root", "password"),
]

# Wordlist for cracking
WORDLIST = [
    '123456', 'password', '12345', '123', 'test', 'hello',
    'qwerty', 'letmein', '123456789', '12345678', 'admin',
    'welcome', 'monkey', 'dragon', 'master', 'pass', 'sunshine',
    'princess', 'football', '1234567890', 'baseball', 'iloveyou',
    'trustno1', 'shadow', 'ashley', 'michael', 'superman'
]

class PasswordSecurityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Security Analysis - CA Project")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")

        self.cracked_passwords = {}
        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="POST-BREACH PASSWORD SECURITY ANALYSIS",
            font=("Arial", 18, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        title_label.pack(pady=10)

        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="Simulated Breach Analysis | MD5 Hash Cracking | Policy Evaluation",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#888"
        )
        subtitle.pack(pady=5)

        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel - Hash Input
        left_panel = tk.Frame(main_frame, bg="#1a1a2e")
        left_panel.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(left_panel, text="Enter Hash to Crack:", font=("Arial", 12, "bold"),
                 bg="#1a1a2e", fg="white").pack(pady=5)

        self.hash_entry = tk.Entry(left_panel, font=("Arial", 11), width=40)
        self.hash_entry.pack(pady=5)

        crack_btn = tk.Button(
            left_panel,
            text="CRACK HASH",
            font=("Arial", 12, "bold"),
            bg="#e94560",
            fg="white",
            command=self.crack_single_hash,
            width=15
        )
        crack_btn.pack(pady=10)

        self.result_label = tk.Label(
            left_panel,
            text="Result: Not cracked yet",
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="#00ff00"
        )
        self.result_label.pack(pady=10)

        # Crack All Button
        crack_all_btn = tk.Button(
            left_panel,
            text="CRACK ALL (Demo)",
            font=("Arial", 11, "bold"),
            bg="#4a4a6a",
            fg="white",
            command=self.crack_all_hashes,
            width=20
        )
        crack_all_btn.pack(pady=20)

        # Right panel - Results Table
        right_panel = tk.Frame(main_frame, bg="#1a1a2e")
        right_panel.pack(side="right", fill="both", expand=True, padx=5)

        tk.Label(right_panel, text="Cracked Passwords:", font=("Arial", 12, "bold"),
                 bg="#1a1a2e", fg="white").pack(pady=5)

        # Treeview for results
        columns = ("Hash", "Username", "Password", "Status")
        self.tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=15)

        self.tree.heading("Hash", text="Hash (truncated)")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.heading("Status", text="Status")

        self.tree.column("Hash", width=120)
        self.tree.column("Username", width=100)
        self.tree.column("Password", width=100)
        self.tree.column("Status", width=80)

        self.tree.pack(fill="both", expand=True)

        # Stats panel at bottom
        self.create_stats_panel()

    def create_stats_panel(self):
        stats_frame = tk.Frame(self.root, bg="#16213e", height=80)
        stats_frame.pack(fill="x", side="bottom")

        # Stats
        self.total_label = tk.Label(stats_frame, text="Total Hashes: 20",
                                     font=("Arial", 11), bg="#16213e", fg="white")
        self.total_label.pack(side="left", padx=30, pady=20)

        self.cracked_label = tk.Label(stats_frame, text="Cracked: 0",
                                       font=("Arial", 11), bg="#16213e", fg="#00ff00")
        self.cracked_label.pack(side="left", padx=30, pady=20)

        self.time_label = tk.Label(stats_frame, text="Time: 0 seconds",
                                    font=("Arial", 11), bg="#16213e", fg="white")
        self.time_label.pack(side="left", padx=30, pady=20)

        self.risk_label = tk.Label(stats_frame, text="RISK LEVEL: UNKNOWN",
                                    font=("Arial", 12, "bold"), bg="#16213e", fg="#ff0000")
        self.risk_label.pack(side="right", padx=30, pady=20)

    def crack_hash(self, target_hash):
        """Try to crack a single hash"""
        for password in WORDLIST:
            computed = hashlib.md5(password.encode()).hexdigest()
            if computed == target_hash:
                return password
        return None

    def play_audio(self, filepath, duration_seconds=None):
        """Play audio file for specified duration (or until finished)"""
        if not HAS_PYGAME:
            return
        if not os.path.exists(filepath):
            print(f"Audio file not found: {filepath}")
            return

        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            if duration_seconds:
                time.sleep(duration_seconds)
                pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error playing audio: {e}")

    def crack_single_hash(self):
        hash_input = self.hash_entry.get().strip()

        if not hash_input:
            messagebox.showwarning("Input Error", "Please enter a hash!")
            return

        # Play 1st audio for 32 seconds while processing
        if HAS_PYGAME:
            threading.Thread(target=self.play_audio, args=(AUDIO_START, 32), daemon=True).start()

        # Wait 32 seconds
        time.sleep(32)

        result = self.crack_hash(hash_input)

        if result:
            # Play 2nd audio when cracked
            if HAS_PYGAME:
                threading.Thread(target=self.play_audio, args=(AUDIO_CRACKED, 5), daemon=True).start()
            self.result_label.config(text=f"Result: {result}", fg="#00ff00")
            messagebox.showinfo("Success", f"Password cracked: {result}")
        else:
            # Play 3rd audio when not cracked
            if HAS_PYGAME:
                threading.Thread(target=self.play_audio, args=(AUDIO_NOT_CRACKED, 5), daemon=True).start()
            self.result_label.config(text="Result: Not found in wordlist", fg="#ff0000")
            messagebox.showerror("Failed", "Password not cracked - not in wordlist")

    def crack_all_hashes(self):
        import time

        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        start_time = time.time()
        cracked_count = 0

        for hash_val, username, expected in BREACH_DATA:
            result = self.crack_hash(hash_val)

            if result:
                status = "CRACKED"
                self.tree.insert("", "end", values=(hash_val[:25] + "...", username, result, status))
                cracked_count += 1
                self.cracked_passwords[username] = result
            else:
                status = "FAILED"
                self.tree.insert("", "end", values=(hash_val[:25] + "...", username, "???", status))

        end_time = time.time()
        elapsed = end_time - start_time

        # Update stats
        self.total_label.config(text=f"Total Hashes: {len(BREACH_DATA)}")
        self.cracked_label.config(text=f"Cracked: {cracked_count} ({cracked_count*100//len(BREACH_DATA)}%)")
        self.time_label.config(text=f"Time: {elapsed:.4f} seconds")
        self.risk_label.config(text="RISK LEVEL: CRITICAL")

        messagebox.showinfo("Complete", f"Cracked {cracked_count}/{len(BREACH_DATA)} passwords in {elapsed:.4f} seconds!")

        # Show analysis
        self.show_analysis()

    def show_analysis(self):
        analysis = """
SECURITY ANALYSIS RESULTS
=========================

Hash Algorithm: MD5 (INSECURE)
Salt: NONE (Vulnerable to rainbow tables)
Cracking Method: Dictionary Attack

FINDINGS:
• All passwords cracked in <1 second
• Using common dictionary words only
• Password length range: 3-10 characters
• No special characters or complexity
• No password policy enforcement

RISK LEVEL: CRITICAL (9.8/10)

RECOMMENDATIONS:
1. Migrate to bcrypt or Argon2 immediately
2. Implement unique salt per password
3. Enforce minimum 12-character passwords
4. Implement account lockout (5 attempts)
5. Deploy Multi-Factor Authentication (MFA)
"""
        messagebox.showinfo("Analysis Results", analysis)


def main():
    root = tk.Tk()
    app = PasswordSecurityGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()