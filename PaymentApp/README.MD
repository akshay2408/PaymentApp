1. Install dependencies. -> Activate env. 
2. Run APIs -> Project root direct ->  run command-> python app.py
3. To run unit testcases -> run command-> pytest --setup-show test_unittest_payment.py
4. To run API testcases -> run command->pytest --setup-show test_api.py

5. API PAYMENT: 
	URL : http://127.0.0.1:5000/api/v1/payment (POST)
	REQUEST : 
		{ "creditCardNumber": "6069980060280276",
        "cardHolder": 12222.5,
        "expirationDate": "11/25",
        "securityCode": "234",
        "amount": 501.7}
