"""
Test pydantic schemas validation
"""

from app.schemas.user import UserCreate, UserLogin, UserUpdate
from pydantic import ValidationError


def test_user_create_valid():
    """Test valid user creation"""
    data = {
        "username": "adityagurram",
        "email": "adityagurrram@gmail.com",
        "password": "aditya6248",
        "display_name": "Aditya Gurram",
    }
    user = UserCreate(**data)
    print(f"valid UserCreate: {user.username}")


def test_user_create_invalid():
    """Test invalid user creation"""
    test_cases = [
        # invalid username
        {
            "username": "ad",
            "email": "adityaguuram@gmail.com",
            "password": "securepassword",
            "display_name": "Adi",
        },
        # invalid email
        {
            "username": "aditya",
            "email": "adi-g",
            "password": "securepassword",
            "display_name": "Adi",
        },
        # invalid password
        {
            "username": "aditya",
            "email": "adityaguuram@gmail.com",
            "password": "invali",
            "display_name": "Adi",
        },
        # invalid username (special chars)
        {
            "username": "aditya@ultrapromax",
            "email": "adityaguuram@gmail.com",
            "password": "securepassword",
            "display_name": "Adi",
        },
    ]

    for i, data in enumerate(test_cases):
        try:
            UserCreate(**data)
            print(f"Test {i} should have failed but passed!!1")
        except ValidationError as e:
            print(f"Testcase {i} correctly rejected: {e.errors()[0]['msg']}")


def test_user_update():
    update = UserUpdate(display_name="aditya gurram")
    print(f"Valid UserUpdate: {update.display_name}")

    update_empty = UserUpdate()
    print("Empty UserUpdate is valid.")


if __name__ == "__main__":
    print("Testing pydantic schemas")

    print("1. Testing UserCreate (Valid):")
    test_user_create_valid()
    print("2. Testing UserCreate (invalid)")
    test_user_create_invalid()
    print("3. Testing UserUpdate (valid)")
    test_user_update()
    print("Schema validation test complete!!")
