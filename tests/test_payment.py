import requests

BASE_URL = "http://127.0.0.1:8000"

def test_create_payment():
    response = requests.post(f"{BASE_URL}/createPayment?amount=500&userId=101")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert "paymentId" in data


def test_invalid_amount():
    response = requests.post(f"{BASE_URL}/createPayment?amount=0&userId=101")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data


def test_payment_flow():
    # Create Payment
    response = requests.post(f"{BASE_URL}/createPayment?amount=300&userId=202")
    payment_id = response.json()["paymentId"]

    # Check Status
    status_response = requests.get(f"{BASE_URL}/paymentStatus/{payment_id}")
    assert status_response.json()["status"] == "SUCCESS"

    # Refund
    refund_response = requests.post(f"{BASE_URL}/refund/{payment_id}")
    assert refund_response.json()["status"] == "REFUNDED"