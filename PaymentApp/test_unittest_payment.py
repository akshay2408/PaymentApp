import pytest
from app import ProcessPayment
from providers import CheapPaymentGateway, PremiumPaymentGateway, ExpensivePaymentGateway
import requests
import json


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


def test_process_cheap_payment_gateway(request_data):
	request_data["amount"] = 14
	provider = {"provider": CheapPaymentGateway(), "retry" : 0}
	pp = ProcessPayment()
	assert PAYMENT_PROCESSED == pp.process(provider, request_data)


def test_process_expensive_payment_gateway(request_data):
	request_data["amount"] = 56
	provider = {"provider": ExpensivePaymentGateway(), "retry" : 0}
	pp = ProcessPayment()
	assert PAYMENT_PROCESSED == pp.process(provider, request_data)


def test_process_premium_payment_gateway(request_data):
	request_data["amount"] = 1023
	provider = {"provider": PremiumPaymentGateway(), "retry" : 3}
	pp = ProcessPayment()
	assert PAYMENT_PROCESSED == pp.process(provider, request_data)


