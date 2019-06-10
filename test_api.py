#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
from apiserver import checkLimits

class TestCheckLimits(unittest.TestCase):
	def test_NumberValue(self):
		#check with number value
		pass

	def test_CheckWrongValue(self):
		#check with non number and negatives.
		self.assertRaises(ValueError, checkLimits, -1, -1)
		self.assertRaises(ValueError, checkLimits, -1, 'abcd')
		self.assertRaises(ValueError, checkLimits, 'abcd', 'abcd')
		self.assertRaises(ValueError, checkLimits, 'abcd', -1)
		self.assertRaises(ValueError, checkLimits, 1001, 1000)




class TestCheckCard(unittest.TestCase):
	def test_checkCard(self):
		pass







class TestCheckFirstTransaction(unittest.TestCase):
	def test_checkFirstTransaction(self):
		pass





class TestSecurityCheckMerchant(unittest.TestCase):
	def test_securityCheckMerchant(self):
		pass




class TestSecurityMerchantDenyList(unittest.TestCase):
	def test_securityMerchantDenyList(self):
		pass



class TestSecurityTransactionInterval(unittest.TestCase):
	def test_securityTransactionInterval(self):
		pass