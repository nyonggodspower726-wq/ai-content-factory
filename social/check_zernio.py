import os
import requests


API_KEY = os.getenv("ZERNIO_API_KEY")

BASE_URL = "https://api.zernio.com/api/v1"


if not API_KEY:
    raise RuntimeError(
        "ZERNIO_API_KEY is missing from Railway Variables."
    )


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


print("=" * 60)
print("ZERNIO CONNECTED ACCOUNTS CHECK")
print("=" * 60)


response = requests.get(
    f"{BASE_URL}/accounts",
    headers=headers,
    timeout=30,
)


print("HTTP STATUS:", response.status_code)
print("RESPONSE:")
print(response.text)

print("=" * 60)
