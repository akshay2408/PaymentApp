import pytest
from app import ProcessPayment
from providers import CheapPaymentGateway, PremiumPaymentGateway, ExpensivePaymentGateway
import requests
import json


url = 'http://127.0.0.1:5000/api/v1/payment'

PAYMENT_PROCESSED = ({"message:" : "Payment is processed."}, 200)
INVALID_REQUEST = ({"error:" : ["The request is invalid."]}, 400)
INTERAL_SERVER_ERROR = ({"error:" : ["An error occur while processing the request."]}, 500)

@pytest.fixture(scope='module')
def request_data():
    payment_info = {    "creditCardNumber": "6069980060280276",
				        "cardHolder": 12222.5,
				        "expirationDate": "11/25",
				        "securityCode": "234",
				        "amount": 501.7 }
    return payment_info


def test_invalid_credit_card_number(request_data):
	request_data["creditCardNumber"] = "sadndnsad636363"
	res_data = requests.post(url, data = request_data)
	assert 500 == res_data.status_code


def test_validation_credit_card_number(request_data):
	request_data["creditCardNumber"] = "6069980060280276"
	res_data = requests.post(url, data = request_data)
	assert 200 == res_data.status_code
	json_response=json.dumps(res_data.json())


def test_validation_invalid_expiration_date(request_data):
	request_data["expirationDate"]= "25/00"
	res_data = requests.post(url, data = request_data)
	json_response=json.dumps(res_data.json())
	assert 500 == res_data.status_code

def test_validation_mandatory_data(request_data):
	del request_data["expirationDate"]
	res_data = requests.post(url, data = request_data)
	json_response=json.dumps(res_data.json())
	assert 500 == res_data.status_code

	del request_data["creditCardNumber"]
	res_data = requests.post(url, data = request_data)
	json_response=json.dumps(res_data.json())
	assert 500 == res_data.status_code

	del request_data["amount"]
	res_data = requests.post(url, data = request_data)
	json_response=json.dumps(res_data.json())
	assert 500 == res_data.status_code

	del request_data["cardHolder"]
	res_data = requests.post(url, data = request_data)
	json_response=json.dumps(res_data.json())
	assert 500 == res_data.status_code






















