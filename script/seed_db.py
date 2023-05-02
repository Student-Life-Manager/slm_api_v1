import sys

import requests

BASE_URL = "http://localhost:8000"
STUDENT_UUID = ""
ACCESS_TOKEN = ""
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

relations = ["brother", "mom", "dad", "sister", "cousin"]
phone_numbers = ["897543344", "986403821", "769986364", "685890002", "788887433"]

if not STUDENT_UUID:
    print("SET STUDENT UUID.")
    sys.exit()

if not ACCESS_TOKEN:
    print("SET ACCESS TOKEN")
    sys.exit()


def create_guardians():
    for i in range(0, 5):
        guardian_payload = {
            "relation": relations[i],
            "phone_number": f"+91{phone_numbers[i]}",
        }

        response = requests.post(
            f"{BASE_URL}/guardian", json=guardian_payload, headers=HEADERS
        )

        if response.status_code != 200:
            print("CREATING GUARDIANS FAILED\n")
            print(response.status_code)
            print(response.json())
            return

        print(f"GUARDIAN {i + 1}:")
        print(response.json())
        print("\n")


create_guardians()
