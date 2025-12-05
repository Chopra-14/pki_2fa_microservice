import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.crypto_utils import load_private_key, decrypt_seed

def main():
    private_key = load_private_key()
    with open("encrypted_seed.txt", "r", encoding="utf-8") as f:
        encrypted_seed = f.read().strip()

    hex_seed = decrypt_seed(encrypted_seed, private_key)
    print("Decrypted seed:", hex_seed)
    print("Length:", len(hex_seed))

if __name__ == "__main__":
    main()
