#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
from datetime import datetime
import re

app = Flask(__name__)
api = Api(app)

#1. The transaction amount should not be above limit

def checkLimits(self, checklimits):
	if self.amount > self.limit:
		return "You can't exceed your limit"
	else:
		return True
		

#2. No transaction should be approved when the card is blocked

def checkCard(self, checkCard):
	if self.cardIsActive !=  True:
		return "Your card is blocked"
	else:
		return True
	

#3. The first transaction shouldn't be above 90% of the limit

def firstTransaction(self, firstTransaction):
	if (self.firstTransaction):
		if self.amount > self.limit * 0.9:
			return "You cant use more than 90% of your limit on your first transaction"
		else:
			return True

#4. There should not be more than 10 transactions on the same merchant

def securityCheckMerchant(self, securityCheckMerchant):
	count=0
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
		return "There should not be more than 10 transactions on the same merchant"
	else: 
		return True
	 
#5. Merchant denylist
def securityMerchantDenyList(self, securityMerchantDenyList):
	
	a = self.denylist.find(self.merchant) #find() will return -1 if merchant is not found
	if a!=-1:          
	   return "This merchant is in our deny list"
	else:
		return True

#6. There should not be more than 3 transactions on a 2 minutes interval   
def securityTransactionInterval(self, securityTransactionInterval):

	if (self.lastTransactions):
		
		#get the third transaction datetime

		thirdLastTransaction = self.lastTransactions[2] 
				
		if (thirdLastTransaction):
			fmt = '%Y-%m-%d %H:%M:%S'
			thirdLastTransactionDateTime = re.findall(r'\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2}', thirdLastTransaction)	
			d1 = datetime.strptime(thirdLastTransactionDateTime[0], fmt)
			d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)

			intervalSinceThirdTransaction = (d2-d1).seconds /60

			if intervalSinceThirdTransaction <= 2:
				return "Too many transactions in 2 minutes interval"
			else:
				return True


class authorization(Resource):
	def post(self):
		print(request.json)
		cardIsActive = request.json[0]['cardIsActive']
		limit = request.json[0]['limit']
		denylist = request.json[0]['denylist']
		isInsideAllowlist = request.json[0]['isInsideAllowlist']
		merchant = request.json[1]['merchant']
		amount = request.json[1]['amount']
		time = request.json[1]['time']
		if (request.json[2]['lastTransactions']):
			lastTransactions = request.json[2]['lastTransactions']
		else:
			firstTransaction = True    
		
		return {'status':'success'}
		



#Api Routes
api.add_resource(authorization, '/authorization')


if __name__ == '__main__':
     app.run()