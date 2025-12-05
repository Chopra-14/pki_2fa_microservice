import os
import sys
import subprocess
import base64
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.crypto_utils import (
    load_private_key,
    load_public_key,
    sign_message,
    encrypt_with_public_key,
)


def get_latest_commit_hash() -> str:
    """
    Get the latest commit hash (40-char hex) using git.
    """
    try:
        output = subprocess.check_output(
            ["git", "log", "-1", "--format=%H"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to get git commit hash: {e}")

    if len(output) != 40:
        raise ValueError(f"Commit hash is not 40 chars: {output}")
    try:
        int(output, 16)
    except ValueError:
        raise ValueError(f"Commit hash is not valid hex: {output}")

    return output


def main():
    commit_hash = get_latest_commit_hash()
    print(f"Commit Hash: {commit_hash}")

    private_key = load_private_key("student_private.pem")

    signature = sign_message(commit_hash, private_key)


    instructor_public_key = load_public_key("instructor_public.pem")
    encrypted_signature_bytes = encrypt_with_public_key(signature, instructor_public_key)
    encrypted_signature_b64 = base64.b64encode(encrypted_signature_bytes).decode("utf-8")

    print("\nEncrypted Commit Signature (Base64, single line):")
    print(encrypted_signature_b64)


if __name__ == "__main__":
    main()
