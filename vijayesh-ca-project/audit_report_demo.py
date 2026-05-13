# Technical Audit Report - Interactive Demo
# Password Security Analysis - CA Project

import hashlib

# Sample hashes from the audit
HASHES = {
    "admin": "21232f297a57a5a743894a0e4a801fc3",
    "jsmith": "5f4dcc3b5aa765d61d8327deb882cf99",
    "dcollins": "40bd001563085fc35165329ea1ff5c5ecbdbbeef",
    "mrodriguez": "ef92b778ba7157967a9c66062cd006877796464673550772792626e25732165c",
    "lwalker": "$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy"
}

# Common passwords for dictionary attack
WORDLIST = [
    'admin', 'password', '123456', '12345678', '123456789',
    'welcome', 'monkey', 'dragon', 'master', 'letmein',
    'shadow', 'sunshine', 'princess', 'football', 'baseball',
    'iloveyou', 'trustno1', 'superman', 'batman', 'admin123'
]

def identify_hash_type(hash_val):
    """Identify hash type based on format"""
    if hash_val.startswith('$2'):
        return "bcrypt"
    elif len(hash_val) == 32:
        return "MD5"
    elif len(hash_val) == 40:
        return "SHA-1"
    elif len(hash_val) == 64:
        return "SHA-256"
    return "Unknown"

def crack_md5_sha1_sha256(target_hash):
    """Try to crack MD5, SHA-1, or SHA-256"""
    for password in WORDLIST:
        # Try MD5
        if len(target_hash) == 32:
            if hashlib.md5(password.encode()).hexdigest() == target_hash:
                return password, "MD5"
        # Try SHA-1
        elif len(target_hash) == 40:
            if hashlib.sha1(password.encode()).hexdigest() == target_hash:
                return password, "SHA-1"
        # Try SHA-256
        elif len(target_hash) == 64:
            if hashlib.sha256(password.encode()).hexdigest() == target_hash:
                return password, "SHA-256"
    return None, None

def main():
    print("\n" + "="*70)
    print("       PASSWORD SECURITY AUDIT - CRACKING SIMULATION")
    print("="*70)
    print()

    cracked_count = 0
    secure_count = 0

    for username, hash_val in HASHES.items():
        hash_type = identify_hash_type(hash_val)

        print(f"User: {username}")
        print(f"Hash Type: {hash_type}")
        print(f"Hash: {hash_val[:40]}...")

        if hash_type == "bcrypt":
            print("Status: SECURE (bcrypt with salt)")
            print("Crack Time: 3-10+ years (not practical)")
            secure_count += 1
        else:
            password, algo = crack_md5_sha1_sha256(hash_val)
            if password:
                print(f"Status: CRACKED!")
                print(f"Password: {password}")
                print(f"Algorithm: {algo}")
                cracked_count += 1
            else:
                print("Status: Not in demo wordlist")
                print("(Would crack with larger wordlist like RockYou)")

        print("-" * 70)

    print("\n" + "="*70)
    print("                        AUDIT SUMMARY")
    print("="*70)
    print(f"Total Users: {len(HASHES)}")
    print(f"Cracked: {cracked_count} (insecure hashing)")
    print(f"Secure: {secure_count} (bcrypt with salt)")
    print(f"Risk Level: CRITICAL (80% vulnerable)")
    print()
    print("RECOMMENDATIONS:")
    print("1. Migrate ALL users to bcrypt/Argon2")
    print("2. Use unique salt per password")
    print("3. Enforce minimum 12-character passwords")
    print("4. Deploy MFA immediately")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()