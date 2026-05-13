# Password Security Analysis - Interactive Console GUI
# CA Project - Works without tkinter!

import hashlib
import time
import os

# Clear screen function
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Sample hashes for demo
BREACH_DATA = {
    "admin": ("21232f297a57a5a743894a0e4a801fc3", "MD5"),
    "jsmith": ("5f4dcc3b5aa765d61d8327deb882cf99", "MD5"),
    "dcollins": ("40bd001563085fc35165329ea1ff5c5ecbdbbeef", "SHA-1"),
    "mrodriguez": ("ef92b778ba7157967a9c66062cd006877796464673550772792626e25732165c", "SHA-256"),
    "lwalker": ("$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy", "bcrypt"),
}

WORDLIST = [
    'admin', 'password', '123456', '12345', '123', 'test', 'hello',
    'qwerty', 'letmein', '123456789', '12345678', 'welcome', 'monkey',
    'dragon', 'master', 'pass', 'sunshine', 'princess', 'admin123', 'letmein123'
]

def print_header():
    clear()
    print("="*70)
    print("       PASSWORD SECURITY ANALYSIS - INTERACTIVE GUI")
    print("       CA Project - Cyber Security Forensics")
    print("="*70)
    print()

def print_menu():
    print("+==================================================================+")
    print("|                        MAIN MENU                                |")
    print("+==================================================================+")
    print("|  [1] View All Hashes                                            |")
    print("|  [2] Crack a Single Hash (Manual Input)                         |")
    print("|  [3] Auto-Crack All Hashes (Dictionary Attack)                 |")
    print("|  [4] Learn About Hash Types                                    |")
    print("|  [5] Security Recommendations                                  |")
    print("|  [6] Exit                                                       |")
    print("+==================================================================+")
    print()

def view_hashes():
    print_header()
    print("BREACH DATA - PASSWORD HASHES")
    print("-"*70)
    print(f"{'Username':<15} {'Hash Type':<10} {'Hash':<40}")
    print("-"*70)
    for user, (hash_val, algo) in BREACH_DATA.items():
        print(f"{user:<15} {algo:<10} {hash_val[:40]}...")
    print()
    input("Press Enter to continue...")

def crack_manual():
    print_header()
    print("CRACK A SINGLE HASH")
    print("-"*70)

    # Show available hashes
    print("Available hashes to crack:")
    for i, (user, (h, a)) in enumerate(BREACH_DATA.items(), 1):
        print(f"  {i}. {user} ({a})")

    print("\nOr enter your own hash to crack!")
    choice = input("\nEnter hash to crack (or number): ").strip()

    # Try to find in our data
    cracked = None

    # Check if it's one of our hashes
    for user, (h, a) in BREACH_DATA.items():
        if choice.lower() == h.lower() or choice == user:
            print(f"\nCracking hash for {user}...")
            time.sleep(0.5)
            # Try wordlist
            for pwd in WORDLIST:
                if a == "MD5":
                    if hashlib.md5(pwd.encode()).hexdigest() == h:
                        cracked = (user, pwd, a)
                        break
                elif a == "SHA-1":
                    if hashlib.sha1(pwd.encode()).hexdigest() == h:
                        cracked = (user, pwd, a)
                        break

    if not cracked:
        # Try user input as password
        password = choice
        for user, (h, a) in BREACH_DATA.items():
            if a == "MD5":
                if hashlib.md5(password.encode()).hexdigest() == h:
                    cracked = (user, password, a)
                    break

    if cracked:
        print(f"\n✅ SUCCESS! Password found: {cracked[1]}")
        print(f"   User: {cracked[0]}, Algorithm: {cracked[2]}")
    else:
        print("\n❌ Password not found in our wordlist")
        print("   (Would crack with larger wordlist like rockyou.txt)")

    print("\nTry these: admin, password, 123456, test, hello, qwerty")
    input("\nPress Enter to continue...")

def auto_crack():
    print_header()
    print("AUTO-CRACKING ALL HASHES (Dictionary Attack)")
    print("-"*70)
    print("Using wordlist:", len(WORDLIST), "common passwords")
    print()

    cracked_count = 0
    results = []

    for user, (hash_val, algo) in BREACH_DATA.items():
        print(f"Cracking {user}'s {algo} hash...", end=" ")
        found = None

        if algo == "bcrypt":
            print("bcrypt - SKIPPED (secure)")
            results.append((user, algo, "SECURE", "3-10+ years"))
            continue

        for pwd in WORDLIST:
            if algo == "MD5":
                if hashlib.md5(pwd.encode()).hexdigest() == hash_val:
                    found = pwd
                    break
            elif algo == "SHA-1":
                if hashlib.sha1(pwd.encode()).hexdigest() == hash_val:
                    found = pwd
                    break
            elif algo == "SHA-256":
                if hashlib.sha256(pwd.encode()).hexdigest() == hash_val:
                    found = pwd
                    break

        if found:
            print(f"FOUND: {found}")
            results.append((user, algo, found, "< 1 second"))
            cracked_count += 1
        else:
            print("Not in wordlist")
            results.append((user, algo, "???", "Vulnerable"))

    print("\n" + "="*70)
    print("                         RESULTS SUMMARY")
    print("="*70)
    print(f"Total Hashes: {len(BREACH_DATA)}")
    print(f"Cracked: {cracked_count}")
    print(f"Secure: {len(BREACH_DATA) - cracked_count - 1}")  # -1 for bcrypt
    print(f"Risk Level: CRITICAL" if cracked_count > 0 else "SECURE")
    print()

    print("DETAILED RESULTS:")
    print("-"*70)
    for user, algo, pwd, time_taken in results:
        status = "[CRACKED]" if pwd != "???" and algo != "bcrypt" else ("[SECURE]" if algo == "bcrypt" else "[VULNERABLE]")
        print(f"{user:<15} {algo:<10} -> {pwd:<15} {status}")

    print()
    input("Press Enter to continue...")

def learn_hash_types():
    print_header()
    print("LEARN ABOUT HASH TYPES")
    print("="*70)

    info = """
    +=======================================================================+
    |                        HASH TYPES EXPLAINED                          |
    +=======================================================================+
    |                                                                       |
    |  MD5 (Message Digest 5)                                              |
    |  * 128-bit hash (32 hex characters)                                 |
    |  * CRITICAL RISK - Can compute 10 billion/second on GPU            |
    |  * No salt - vulnerable to rainbow tables                           |
    |  * Crack time: < 1 second                                           |
    |                                                                       |
    |  SHA-1 (Secure Hash Algorithm 1)                                    |
    |  * 160-bit hash (40 hex characters)                                 |
    |  * CRITICAL RISK - Deprecated by NIST since 2011                   |
    |  * Similar problems as MD5                                          |
    |  * Crack time: < 1 second                                           |
    |                                                                       |
    |  SHA-256                                                             |
    |  * 256-bit hash (64 hex characters)                                 |
    |  * HIGH RISK - Better than MD5/SHA-1 but still unsuitable           |
    |  * No salt - still vulnerable                                        |
    |  * Crack time: ~1 second with GPU                                    |
    |                                                                       |
    |  bcrypt                                                              |
    |  * Based on Blowfish cipher                                         |
    |  * SECURE - Has built-in salt (128-bit)                             |
    |  * Work factor (cost) slows down attackers                          |
    |  * Crack time: 3-10+ YEARS (not practical)                          |
    |                                                                       |
    +=======================================================================+
    """
    print(info)

    print("KEY CONCEPT - SALT:")
    print("-"*70)
    print("WITHOUT SALT:")
    print("  'password' → 5f4dcc3b5aa765d61d8327deb882cf99")
    print("  'password' → 5f4dcc3b5aa765d61d8327deb882cf99")
    print("  (Same password = Same hash! Easy to crack!)")
    print()
    print("WITH SALT (bcrypt):")
    print("  'password' + salt1 → $2a$10$abc123... (unique)")
    print("  'password' + salt2 → $2a$10$xyz789... (unique)")
    print("  (Same password = Different hashes! Hard to crack!)")
    print()

    input("Press Enter to continue...")

def show_recommendations():
    print_header()
    print("SECURITY RECOMMENDATIONS (Based on NIST Guidelines)")
    print("="*70)

    rec = """
    +=======================================================================+
    |                   3-POINT IMPROVED PASSWORD POLICY                    |
    +=======================================================================+
    |                                                                       |
    |  POINT 1: LENGTH OVER COMPLEXITY                                     |
    |  -------------------------------------------                          |
    |  [X] OLD: Require uppercase, lowercase, number, special             |
    |  [OK] NEW: Minimum 12 characters (16+ recommended)                  |
    |                                                                       |
    |  Why? "CorrectHorseBatteryStaple" (25 chars) is stronger than        |
    |       "P@ssw0rd1!" (10 chars) - length beats complexity!            |
    |                                                                       |
    +=======================================================================+
    |  POINT 2: MODERN HASHING                                            |
    |  -------------------------                                           |
    |  [X] OLD: MD5, SHA-1, SHA-256 (fast, no salt)                      |
    |  [OK] NEW: bcrypt or Argon2id (slow, built-in salt)                |
    |                                                                       |
    |  Why? bcrypt takes 3-10+ years to crack vs <1 second for MD5!       |
    |                                                                       |
    +=======================================================================+
    |  POINT 3: BREACH DETECTION + MFA                                    |
    |  ---------------------------------                                    |
    |  [X] OLD: Just password                                             |
    |  [OK] NEW: Check HaveIBeenPwned + Multi-Factor Authentication       |
    |                                                                       |
    |  Why? Even if password cracks, MFA stops attackers!                  |
    |                                                                       |
    +=======================================================================+

    IMMEDIATE ACTIONS REQUIRED:
    ---------------------------
    1. Force password reset for MD5/SHA-1 users
    2. Migrate to bcrypt immediately
    3. Implement account lockout (5 attempts, 15 min)
    4. Deploy MFA for all users
    """
    print(rec)

    input("Press Enter to continue...")

def main():
    while True:
        print_header()
        print_menu()

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            view_hashes()
        elif choice == "2":
            crack_manual()
        elif choice == "3":
            auto_crack()
        elif choice == "4":
            learn_hash_types()
        elif choice == "5":
            show_recommendations()
        elif choice == "6":
            print("\nThank you for using Password Security Analysis!")
            print("Good luck with your CA Project! 🎓")
            break
        else:
            print("Invalid choice! Press Enter to try again...")
            input()

if __name__ == "__main__":
    main()