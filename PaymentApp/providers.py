class PremiumPaymentGateway:
	def process(self, data):
		return True

class ExpensivePaymentGateway:
	def process(self, data):
		return True

class CheapPaymentGateway:
	def process(self, data):
		return True