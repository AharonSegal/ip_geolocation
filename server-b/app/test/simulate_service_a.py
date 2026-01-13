# simulate_service_a.py

import requests

SERVICE_B_URL = "http://127.0.0.1:8000/single-ip-from-server-a"

def test_valid_ip():
    payload = {
        "ip": "2.2.2.2",
        "coordinates": {
            "latitude": 40.22228,
            "longitude": -74.2222
        }
    }

    resp = requests.post(SERVICE_B_URL, json=payload)
    print("VALID IP TEST")
    print("Status:", resp.status_code)
    print("Response:", resp.json())
    print("=" * 40)


# def test_invalid_ip():
#     payload = {
#         "ip": "not-an-ip",
#         "coordinates": {
#             "latitude": 40.7128,
#             "longitude": -74.0060
#         }
#     }

#     resp = requests.post(SERVICE_B_URL, json=payload)
#     print("INVALID IP TEST")
#     print("Status:", resp.status_code)
#     print("Response:", resp.json())
#     print("=" * 40)


# def test_invalid_coordinates():
#     payload = {
#         "ip": "8.8.8.8",
#         "coordinates": {
#             "latitude": 999,   # invalid, > 90
#             "longitude": 0
#         }
#     }

#     resp = requests.post(SERVICE_B_URL, json=payload)
#     print("INVALID COORDINATES TEST")
#     print("Status:", resp.status_code)
#     print("Response:", resp.json())
#     print("=" * 40)


if __name__ == "__main__":
    test_valid_ip()
    # test_invalid_ip()
    # test_invalid_coordinates()