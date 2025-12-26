base_url = "https://automationintesting.online"
api_url = f"{base_url}/booking"

admin_credentials = {
    "username": "admin",
    "password": "password"
}

valid_booking_data = {
    "firstname": "Andrii",
    "lastname": "Test",
    "email": "andrii@example.com",
    "phone": "09718618291"
}

invalid_booking_data = {
    "firstname": "",
    "lastname": "",
    "email": "non-an-email",
    "phone": "qwety"
}

room_data = {
    "roomName": "Test Room",
    "type": "Single",
    "accessible": True,
    "description": "Test room for testing purposes",
    "features": ["WiFi", "TV", "Safe"],
    "roomPrice": 100
}
