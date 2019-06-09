#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)

class authorization(Resource):
	def get(self):
        print(request.json)
        cardIsActive = request.json['cardIsActive']
        limit = request.json['limit']
        denylist = request.json['denylist']
        isInsideAllowlist = request.json['isInsideAllowlist']
        merchant = request.json['merchant']
        amount = request.json['amount']
        time = request.json['time']
        if (request.json['lastTransactions']):
   	        lastTransactions = request.json['lastTransactions']
   	    else
   	    	firstTransaction = True    


#1. The transaction amount should not be above limit

	def checklimits(self, checklimits):
		if self.amount > self.limit:
			deniedReasons = "You can't exceed your limit"
		else deniedReasons = " "

#2. No transaction should be approved when the card is blocked

	def checkCard(self, checkCard):
		if self.cardIsActive !=  True:
			deniedReasons = "Your card is blocked"
		else deniedReasons = " "

#3. The first transaction shouldn't be above 90% of the limit

	def firstTransaction(self, firstTransaction):
		if (self.firstTransaction):
			if self.amount > self.limit * 0.9:
				deniedReasons = "You cant use more than 90% of your limit on your first transaction"



#4. There should not be more than 10 transactions on the same merchant

	def securityCheckMerchant(self, securityCheckMerchant):
	count =0
	F=True # just an aux flag 
	P=0 # Just a index position reference
	while F:
	    a = self.lastTransactions.find(self.merchant,P) #find() will return -1 if merchant is not found
	    if a==-1:          
	        F=False
	    else:               # if word is there, increase index counter and stay in loop
	        MtCounter+=1 # Merchant Transaction Counter :P
	        P=a+1

	if MtCounter > 10:
		deniedReasons = "There should not be more than 10 transactions on the same merchant"
	 

#5. Merchant denylist
	def securityMerchantDenyList(self, securityMerchantDenyList):
		
		a = self.denylist.find(self.merchant) #find() will return -1 if merchant is not found
		if a!=-1:          
		   deniedReasons = "This merchant is in our deny list"


api.add_resource(authorization, '/authorization')


if __name__ == '__main__':
     app.run()