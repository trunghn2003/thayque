import requests

patients = [
    {"username": "patient1", "password": "TestPassword123", "email": "patient1@example.com", "user_type": "patient"},
    {"username": "patient2", "password": "TestPassword123", "email": "patient2@example.com", "user_type": "patient"},
    {"username": "patient3", "password": "TestPassword123", "email": "patient3@example.com", "user_type": "patient"},
]

for pat in patients:
    resp = requests.post(
        "http://localhost:8004/api/users/register/",
        json={
            "username": pat["username"],
            "password": pat["password"],
            "password2": pat["password"],
            "email": pat["email"],
            "user_type": pat["user_type"]
        },
        headers={"Content-Type": "application/json"}
    )
    print(f"Tạo user bệnh nhân {pat['username']}: {resp.status_code} {resp.text}")
