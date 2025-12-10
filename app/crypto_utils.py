import json
import pathlib
import requests


API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

STUDENT_ID = "23A91A6127"  
GITHUB_REPO_URL = "https://github.com/Chopra-14/pki-2fa-microservice"


def request_seed(student_id: str, github_repo_url: str, api_url: str = API_URL):
    """
    Request encrypted seed from instructor API and save to encrypted_seed.txt
    """
    public_key_path = pathlib.Path("student_public.pem")

    if not public_key_path.exists():
        raise FileNotFoundError("student_public.pem not found in project root")

    public_key_pem = public_key_path.read_text(encoding="utf-8")


    public_key_single_line = public_key_pem

 
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_single_line,
    }

    print("➡ Sending request to instructor API...")


    try:
        response = requests.post(
            api_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=15,
        )
    except requests.RequestException as e:
        raise SystemError(f"Failed to call instructor API: {e}")


    try:
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError(f"Non-JSON response from API: {response.text}")

  
    if response.status_code != 200 or data.get("status") != "success":
        raise RuntimeError(f"API error: {data}")

    encrypted_seed = data.get("encrypted_seed")
    if not encrypted_seed:
        raise ValueError("API response missing 'encrypted_seed'")
    out_path = pathlib.Path("encrypted_seed.txt")
    out_path.write_text(encrypted_seed.strip(), encoding="utf-8")

    print("✅ Encrypted seed saved to encrypted_seed.txt")
    return encrypted_seed


def main():
    if STUDENT_ID == "YOUR_STUDENT_ID_HERE":
        raise ValueError("Please edit scripts/request_seed.py and set STUDENT_ID first.")

    print(f"Using student_id={STUDENT_ID}")
    print(f"Using github_repo_url={GITHUB_REPO_URL}")

    request_seed(STUDENT_ID, GITHUB_REPO_URL)


if _name_ == "_main_":
    main()
