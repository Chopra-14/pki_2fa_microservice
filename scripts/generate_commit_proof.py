#!/usr/bin/env python3
import os
import sys
import subprocess
import base64
from pathlib import Path

# Make sure we can import from app/
sys.path.append(str(Path(_file_).resolve().parents[1]))

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

    # Simple hex validation
    try:
        int(output, 16)
    except ValueError:
        raise ValueError(f"Commit hash is not valid hex: {output}")

    return output


def main():
    # 1. Get current commit hash
    commit_hash = get_latest_commit_hash()
    print(f"Commit Hash: {commit_hash}")

    # 2. Load student private key
    private_key = load_private_key("student_private.pem")

    # 3. Sign commit hash with student private key (RSA-PSS-SHA256)
    signature = sign_message(commit_hash, private_key)

    # 4. Load instructor public key
    instructor_public_key = load_public_key("instructor_public.pem")

    # 5. Encrypt the signature using instructor public key (RSA/OAEP-SHA256)
    encrypted_signature_bytes = encrypt_with_public_key(signature, instructor_public_key)

    # 6. Base64 encode encrypted signature (single line)
    encrypted_signature_b64 = base64.b64encode(encrypted_signature_bytes).decode("utf-8")

    print("\nEncrypted Commit Signature (Base64, single line):")
    print(encrypted_signature_b64)


if _name_ == "_main_":
    main()
