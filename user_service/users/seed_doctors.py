import requests

doctors = [
    {"username": "doctor1", "password": "TestPassword123", "email": "doctor1@example.com", "user_type": "doctor"},
    {"username": "doctor2", "password": "TestPassword123", "email": "doctor2@example.com", "user_type": "doctor"},
    {"username": "doctor3", "password": "TestPassword123", "email": "doctor3@example.com", "user_type": "doctor"},
]

for doc in doctors:
    resp = requests.post(
        "http://localhost:8004/api/users/register/",
        json={
            "username": doc["username"],
            "password": doc["password"],
            "password2": doc["password"],
            "email": doc["email"],
            "user_type": doc["user_type"]
        },
        headers={"Content-Type": "application/json"}
    )
    print(f"Tạo user bác sĩ {doc['username']}: {resp.status_code} {resp.text}")
