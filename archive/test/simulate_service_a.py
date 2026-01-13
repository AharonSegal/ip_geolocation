import requests

SERVICE_B_URL = "http://127.0.0.1:8000/list-ip-from-server-a"


def test_valid_ip():
    payload = [
        {
            "ip": "2.2.2.2",
            "coordinates": {
                "latitude": 40.22228,
                "longitude": -74.2222,
            },
        },
        {
            "ip": "2.2.2.2",
            "coordinates": {
                "latitude": 40.22228,
                "longitude": -74.2222,
            },
        },
    ]

    resp = requests.post(SERVICE_B_URL, json=payload)

    print("VALID IP TEST")
    print("Status:", resp.status_code)
    print("Headers:", resp.headers)
    print("Raw body:", repr(resp.text))  # <-- see the actual text

    # Try to parse JSON only if it looks like JSON
    try:
        data = resp.json()
        print("Parsed JSON:", data)
    except Exception as e:
        print("Could not parse JSON:", e)

    print("=" * 40)


if __name__ == "__main__":
    test_valid_ip()