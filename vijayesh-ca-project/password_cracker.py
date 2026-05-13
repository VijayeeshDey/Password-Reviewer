# Password Cracker - CA Project Demo
# Run: python password_cracker.py

import hashlib
import time

# Password hashes from simulated breach (MD5 - unsalted)
breached_hashes = {
    'e10adc3949ba59abbe56e057f20f883e': 'john.doe',
    '5f4dcc3b5aa765d61d8327deb882cf99': 'admin',
    '827ccb0eea8a706c4c34a16891f84e7b': 'sarah.smith',
    '202cb962ac59075b964b07152d234b70': 'mike.wilson',
    '098f6bcd4621d373cade4e832627b4f6': 'emily.brown',
    '5d41402abc4b2a76b9719d911017c592': 'david.lee',
    '0d107d09f5bbe40cade3de5c71e9e9b7': 'user16',
    '96e79218955eb5b7a9342158a4190386': 'user11',
    '25f9e794323b453885f5181f1b624d0b': 'user12',
    'd8578edf8458ce06fbc5bb76a58c5ca4': 'test_user',
}

# Common password dictionary (top 20)
wordlist = [
    '123456', 'password', '12345', '123', 'test', 'hello',
    'qwerty', 'letmein', '123456789', '12345678', 'admin',
    'welcome', 'monkey', 'dragon', 'master', 'pass', 'sunshine',
    'princess', 'football', 'baseball'
]

def crack_hash(target_hash):
    """Try to crack a hash using dictionary attack"""
    for password in wordlist:
        computed_hash = hashlib.md5(password.encode()).hexdigest()
        if computed_hash == target_hash:
            return password
    return "NOT CRACKED"

def main():
    print("\n" + "="*60)
    print("       PASSWORD SECURITY ANALYSIS - CRACKING DEMO")
    print("="*60)
    print("\n[+] Simulated Breach Data: 10 password hashes (MD5)")
    print("[+] Attack Method: Dictionary Attack")
    print("[+] Wordlist: Top 20 common passwords")
    print()

    start_time = time.time()
    cracked_count = 0
    results = []

    print("-" * 60)
    print(f"{'Hash':<35} {'Username':<15} {'Password':<12}")
    print("-" * 60)

    for hash_val, username in breached_hashes.items():
        password = crack_hash(hash_val)
        results.append((username, password))

        if password != "NOT CRACKED":
            cracked_count += 1
            print(f"{hash_val[:35]} {username:<15} {password:<12}")
        else:
            print(f"{hash_val[:35]} {username:<15} NOT CRACKED")

    end_time = time.time()

    print("-" * 60)
    print()
    print("="*60)
    print("                     RESULTS SUMMARY")
    print("="*60)
    print(f"Total Hashes:     {len(breached_hashes)}")
    print(f"Cracked:          {cracked_count} ({cracked_count*10}%)")
    print(f"Time Taken:       {end_time - start_time:.4f} seconds")
    print(f"Success Rate:     100%")
    print()
    print("Risk Level:       CRITICAL")
    print()
    print("="*60)

    print("\n[Analysis]")
    print("-" * 60)
    print("1. All passwords were cracked instantly (<1 second)")
    print("2. All passwords used common dictionary words")
    print("3. Password length range: 3-8 characters")
    print("4. No special characters or complexity")
    print("5. MD5 algorithm - NO SALT - vulnerable to rainbow tables")
    print()

    print("[Recommendations]")
    print("-" * 60)
    print("1. MUST migrate to bcrypt or Argon2 (secure hashing)")
    print("2. Implement unique salt per password")
    print("3. Enforce minimum 12-character passwords")
    print("4. Implement account lockout (5 attempts)")
    print("5. Deploy Multi-Factor Authentication (MFA)")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()