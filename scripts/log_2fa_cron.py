import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.totp_utils import generate_totp_code  

def main():
    seed_path = Path("/data/seed.txt")

    if not seed_path.exists():
        print("Seed file not found at /data/seed.txt", file=sys.stderr)
        return

    try:
        hex_seed = seed_path.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"Failed to read seed file: {e}", file=sys.stderr)
        return

    try:
        code = generate_totp_code(hex_seed)
    except Exception as e:
        print(f"Failed to generate TOTP code: {e}", file=sys.stderr)
        return

    now_utc = datetime.now(timezone.utc)
    timestamp = now_utc.strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} - 2FA Code: {code}")


if __name__ == "__main__":
    main()