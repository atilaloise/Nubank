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





api.add_resource(authorization, '/authorization')


if __name__ == '__main__':
     app.run()