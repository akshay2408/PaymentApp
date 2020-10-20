from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from providers import *
import logging
from datetime import datetime
import credit_card_validator as cc_validator

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

PAYMENT_PROCESSED = ({"message:" : "Payment is processed."}, 200)
INVALID_REQUEST = ({"error:" : ["The request is invalid."]}, 400)
INTERAL_SERVER_ERROR = ({"error:" : ["An error occur while processing the request."]}, 500)
DATE_FORMAT = "%m/%y"
PROVIDERS = [PremiumPaymentGateway(), ExpensivePaymentGateway(), CheapPaymentGateway()]


class ProcessPayment(Resource):
    def post(self):
    	try:
    		parser = reqparse.RequestParser(bundle_errors=True)
    		valid_data = self.validate(parser)
    		provider = self.choose_provider(amount=valid_data.get("amount", None))
    		res_body = self.process(provider, valid_data)
    		return res_body
    	except Exception as exp:
    		return {"error:" : [f"{str(exp)}"]}, 500

    def process(self, provider, valid_data):
    	if provider:
    		isProcessed = provider["provider"].process(valid_data)
    		if isProcessed: return PAYMENT_PROCESSED
    		elif not isProcessed and provider["retry"] is 0:
    			return INTERAL_SERVER_ERROR
    		elif provider["retry"] > 0:
    			for i in range(0, (provider["retry"])):
    				isProcessed = provider["provider"].process(valid_data)
    				logging.info(f"retry payment request {i}")
    				if isProcessed :
    					return PAYMENT_PROCESSED
    			if not isProcessed:
    				return INTERAL_SERVER_ERROR
    	else: return INTERAL_SERVER_ERROR

    def check_provider_availability(self, provider):
    	if provider in PROVIDERS:
    		return True
    	else: return False

    def choose_provider(self, amount):
    	CheapPaymentGatewayRule = amount<20
    	ExpensivePaymentGatewayRule = 21 <= amount <= 500
    	PremiumPaymentGatewayRule = amount > 500
    	if CheapPaymentGatewayRule:
    		return {"provider" : PROVIDERS[2], "retry":0}
    	elif ExpensivePaymentGatewayRule:
    		return {"provider" : PROVIDERS[1], "retry":0} if self.check_provider_availability(PROVIDERS[1]) else {"provide" : PROVIDERS[2], "retry":0}
    	elif PremiumPaymentGatewayRule:
    		return {"provider" : PROVIDERS[0], "retry":3}
    	else: return None

    def validate(self, parser):
    	parser.add_argument('creditCardNumber', type=str, required=True,)
    	parser.add_argument('cardHolder', type=str, required=True,)
    	parser.add_argument('expirationDate', type=str, required=True,)
    	parser.add_argument('securityCode', type=str, required=False,)
    	parser.add_argument('amount', type=int, required=True,)

    	res_data= parser.parse_args()

    	if not cc_validator.validate(res_data["creditCardNumber"]): raise Exception(f"Invalid credit card number.")
    	if len(res_data["securityCode"]) is not 3 : raise Exception(f"Invalid security code.")

    	try:
    		date_time_obj = datetime.strptime(res_data["expirationDate"], DATE_FORMAT)
    		res_data["expirationDate"] = date_time_obj
    	except Exception as exp: 
    		raise Exception(f"Invalid expiration date, {str(exp)}")

    	return res_data

    
api.add_resource(ProcessPayment, '/api/v1/payment')

if __name__ == '__main__':
    app.run(debug=True)