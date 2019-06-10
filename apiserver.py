#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
from datetime import datetime
import re


app = Flask(__name__)
api = Api(app)

#1. The transaction amount should not be above limit

def checkLimits(amount, limit):
	#testing
	if type(amount) not in [int, float]:
		raise ValueError("Amount must be integers or float")
	if type(limit) not in [int, float]:
		raise ValueError("Limit must be integers or float")
	if limit < 0:
		raise ValueError("Limit cannot be negative")
	if amount < 0:
		raise ValueError("Amount cannot be negative")
	

	if amount>limit:
		return "You can't exceed your limit"

	else:
		return "True"
		

#2. No transaction should be approved when the card is blocked

def checkCard(cardIsActive):
	
	if cardIsActive == 'True':
		return "True"
	else:
		return "Your card is blocked"
		

#3. The first transaction shouldn't be above 90% of the limit

def checkFirstTransaction(lastTransactions, amount, limit):
	
	if bool(lastTransactions[0]) == False:
		if amount > limit * 0.9:
			return "You cant use more than 90% of your limit on your first transaction"
		else:
			return True
	else:
		return True

#4. There should not be more than 10 transactions on the same merchant

def securityCheckMerchant(lastTransactions, merchant):

	lastTransactions = ', '.join(lastTransactions)  #we need a string to search in

	MtCounter=0
	F=True # just an aux flag 
	P=0 # Just a index position reference
	while F:
	    a = lastTransactions.find(merchant,P) #find() will return -1 if merchant is not found
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
def securityMerchantDenyList(merchant, denylist):
	denylist = ', '.join(denylist)
	# As we use only one merchant in a transaction, we dont need a loop here.
	a = denylist.find(merchant) #find() will return -1 if merchant is not found
	if a!=-1:          
	   return "This merchant is in our deny list"
	else:
		return True

#6. There should not be more than 3 transactions on a 2 minutes interval   
def securityTransactionInterval(lastTransactions, time):

	if (lastTransactions):
		if len(lastTransactions)>2:
			#get the third transaction datetime
			thirdLastTransaction = lastTransactions[2] 
		
			if (thirdLastTransaction):

				fmt = '%Y-%m-%d %H:%M:%S'
				thirdLastTransactionDateTime = re.findall(r'\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2}', thirdLastTransaction)	
				d1 = datetime.strptime(thirdLastTransactionDateTime[0], fmt)
				d2 = datetime.strptime(time, fmt)
				intervalSinceThirdTransaction = (d2-d1).seconds /60
			
				
				if intervalSinceThirdTransaction <= 2:
					return "Too many transactions in 2 minutes interval"
				else:
					return True
			else:
				return True
		else:
			return True
	else:
		return True



class authorization(Resource):
	def post(self):
		#print(request.json)
		#everything is comming as string, so don't forget to convert data types
		#I do not convert booleans because if the variable has a value, python always consider as true. So, let this as string.
		#if there is something specific, we treat on the fly :P
		cardIsActive = request.json[0]['cardIsActive']
		limit = float(request.json[0]['limit'])
		denylist = request.json[0]['denylist']
		isInsideAllowlist = request.json[0]['isInsideAllowlist']
		merchant = request.json[1]['merchant']
		amount = float(request.json[1]['amount'])
		time = request.json[1]['time']
		if (request.json[2]['lastTransactions']) =="":
			lastTransactions = False
		else:
			lastTransactions = request.json[2]['lastTransactions']
		newLimit=limit-amount

		
		checkLimitsOk = checkLimits(amount, limit)
		checkCardOk = checkCard(cardIsActive)
		checkFirstTransactionOk = checkFirstTransaction(lastTransactions, amount, limit)
		securityCheckMerchantOk = securityCheckMerchant(lastTransactions, merchant)
		securityMerchantDenyListsOk = securityMerchantDenyList(merchant, denylist)
		securityTransactionIntervalOk = securityTransactionInterval(lastTransactions, time)

		#everything needs to be true to aprove transaction;
		deniedReasons = []
		approved = True
		if checkLimitsOk != "True":
			deniedReasons.append(checkLimitsOk)
		if checkCardOk != "True":
			deniedReasons.append(checkCardOk)
		if checkFirstTransactionOk != True:
			deniedReasons.append(checkFirstTransactionOk)
		if securityCheckMerchantOk != True:
			deniedReasons.append(securityCheckMerchantOk)
		if securityMerchantDenyListsOk != True:
			deniedReasons.append(securityMerchantDenyListsOk)
		if securityTransactionIntervalOk != True:
			deniedReasons.append(securityTransactionIntervalOk)
		if bool(deniedReasons):
			approved = False
		deniedReasons= ', '.join(deniedReasons)  #we need a string to use with json.loads method 
		output = '{{"approved": "{0}", "newLimit": "{2}", "deniedReasons": "{1}"}}'.format(approved, deniedReasons, newLimit)
		output = json.loads(output)
		return output

#Api Routes
api.add_resource(authorization, '/authorization')
if __name__ == '__main__':
     app.run(debug=True)