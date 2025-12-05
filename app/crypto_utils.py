import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization


def load_private_key(path: str = "student_private.pem"):
    """
    Load RSA private key from PEM file.
    """
    key_path = Path(path)
    if not key_path.exists():
        raise FileNotFoundError(f"{path} not found in project root")

    private_key = serialization.load_pem_private_key(
        key_path.read_bytes(),
        password=None
    )
    return private_key

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP (SHA-256).
    """

    try:
        encrypted_bytes = base64.b64decode(encrypted_seed_b64)
    except Exception:
        raise ValueError("Invalid base64 encrypted seed")

    try:
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise ValueError(f"Seed decryption failed: {e}")

    try:
        hex_seed = decrypted_bytes.decode("utf-8").strip()
    except Exception:
        raise ValueError("Decrypted seed is not valid UTF-8")

    if len(hex_seed) != 64:
        raise ValueError("Decrypted seed must be 64 characters long")

    allowed = "0123456789abcdef"
    if any(c not in allowed for c in hex_seed.lower()):
        raise ValueError("Decrypted seed contains invalid characters (not hex)")

    return hex_seed

def load_public_key(path: str = "instructor_public.pem"):
    """
    Load RSA public key from PEM file.
    """
    key_path = Path(path)
    if not key_path.exists():
        raise FileNotFoundError(f"{path} not found in project root")

    public_key = serialization.load_pem_public_key(key_path.read_bytes())
    return public_key

def sign_message(message: str, private_key) -> bytes:
    """
    Sign a message using RSA-PSS with SHA-256.

    - Message is ASCII/UTF-8 string (NOT hex bytes!)
    - Padding: PSS, MGF1(SHA-256)
    - Salt length: MAX_LENGTH
    """
    message_bytes = message.encode("utf-8")

    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    return signature

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """
    Encrypt data using RSA-OAEP with SHA-256.
    """
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext
