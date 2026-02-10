import secrets

def generate_token():
    return str(secrets.randbelow(900000) + 100000)  # 6‑digit token

print(f"Your token: {generate_token()}")
