#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
from apiserver import checkLimits
from apiserver import checkCard
from apiserver import checkFirstTransaction
from apiserver import securityCheckMerchant
from apiserver import securityMerchantDenyList
from apiserver import securityTransactionInterval

class TestCheckLimits(unittest.TestCase):
	def test_CheckOverLimitValue(self):
		self.assertEqual(checkLimits(1001, 900), False)
		self.assertEqual(checkLimits(1000000, 900), False)
		self.assertEqual(checkLimits(1000.000, 900), False)
		self.assertEqual(checkLimits(1000.0, 900), False)

	def test_CheckUnderLimitValue(self):
		self.assertEqual(checkLimits(100, 900), True)
		self.assertEqual(checkLimits(10, 900), True)
		self.assertEqual(checkLimits(10.000, 900), True)
		self.assertEqual(checkLimits(10.0, 900), True)

	def test_CheckWrongLimitValue(self):
		self.assertRaises(ValueError, checkLimits, -1, -1)
		self.assertRaises(ValueError, checkLimits, -1, 'abcd')
		self.assertRaises(ValueError, checkLimits, 'abcd', 'abcd')
		self.assertRaises(ValueError, checkLimits, 'abcd', -1)
		
class TestCheckCard(unittest.TestCase):
	def test_checkActiveCard(self):
 		self.assertEqual(checkCard(True), True)

	def test_checkInactiveCard(self):
 		self.assertEqual(checkCard(False), False)
	
	def test_checkCardActiveTypeValue(self):
		self.assertRaises(ValueError, checkCard, "12")
		self.assertRaises(ValueError, checkCard, 1)
		self.assertRaises(ValueError, checkCard, 0)
		self.assertRaises(ValueError, checkCard, -1)
		self.assertRaises(ValueError, checkCard, "aeae")

class TestCheckFirstTransaction(unittest.TestCase):
	def test_checkFirstTransaction(self):
 		self.assertEqual(checkFirstTransaction( True, 1000, 1000), True)
 		self.assertEqual(checkFirstTransaction( False, 901, 1000), False)
 		self.assertEqual(checkFirstTransaction( False, 900.1, 1000), False)
 		self.assertEqual(checkFirstTransaction( False, 900, 1000), True)

	def test_checkFirstTransactionTypeValue(self):
		self.assertRaises(ValueError, checkFirstTransaction, "12", 1, 1)
		self.assertRaises(ValueError, checkFirstTransaction, 1, 1, 1)
		self.assertRaises(ValueError, checkFirstTransaction, 0, 1, 1)
		self.assertRaises(ValueError, checkFirstTransaction, -1, 1, 1)
		self.assertRaises(ValueError, checkFirstTransaction, "aeae", 1, 1)

class TestSecurityCheckMerchant(unittest.TestCase):
	def test_securityCheckMerchant(self):
		self.assertEqual(securityCheckMerchant( ["2019-06-09 17:10:32 - boteco do zé", "2019-06-09 16:12:32 - boteco do zé", "2019-06-08 23:59:00 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé"], "boteco do zé"), False)
		self.assertEqual(securityCheckMerchant( ["2019-06-09 17:10:32 - boteco do zé", "2019-06-09 16:12:32 - boteco do zé", "2019-06-08 23:59:00 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé"], "boteco do zé"), True)
		self.assertEqual(securityCheckMerchant( ["2019-06-09 17:10:32 - boteco do zé", "2019-06-09 16:12:32 - boteco do zé", "2019-06-08 23:59:00 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé", "2019-06-09 16:10:32 - boteco do zé"], "boteco do tonho"), True)

	def test_checkFirstTransactionTypeValue(self):
		self.assertRaises(ValueError, securityCheckMerchant, "12", "12")
		self.assertRaises(ValueError, securityCheckMerchant, 1, 1)
		self.assertRaises(ValueError, securityCheckMerchant, 0, 1)
		self.assertRaises(ValueError, securityCheckMerchant, -1, 1)
		self.assertRaises(ValueError, securityCheckMerchant, "aeae", 11)

class TestSecurityMerchantDenyList(unittest.TestCase):
	def test_checkSecurityMerchantDenyList(self):
 		self.assertEqual(securityMerchantDenyList( "Boteco do Tonho", [ "boteco do claudio", "boteco do zé" ]), True)
 		self.assertEqual(securityMerchantDenyList( "Boteco do Tonho", [ "boteco do jão", "boteco do claudio", "Boteco do Tonho" ]), False)
 		
	def test_checkSecurityMerchantDenyListTypeValue(self):
		self.assertRaises(ValueError, securityMerchantDenyList, "12", 1)
		self.assertRaises(ValueError, securityMerchantDenyList, 1, 1)
		self.assertRaises(ValueError, securityMerchantDenyList, 0, 1)
		self.assertRaises(ValueError, securityMerchantDenyList, -1, 1)
		self.assertRaises(ValueError, securityMerchantDenyList, "aeae", 1)

class TestSecurityTransactionInterval(unittest.TestCase):
	def test_checkSecurityTransactionInterval(self):
 		self.assertEqual(securityTransactionInterval(  ["2019-06-09 16:13:10 - boteco do zé", "2019-06-09 16:12:40 - boteco do zé", "2019-06-09 16:12:32 - boteco do zé"], "2019-06-09 16:13:32"), False)
 		self.assertEqual(securityTransactionInterval(  ["2019-06-09 16:13:10 - boteco do zé", "2019-06-09 16:12:40 - boteco do zé", "2019-06-09 16:12:32 - boteco do zé"], "2019-06-09 16:16:32"), True)
 		
	def test_checkSecurityTransactionIntervalTypeValue(self):
		self.assertRaises(ValueError, securityTransactionInterval, "12", 1)
		self.assertRaises(ValueError, securityTransactionInterval, 1, 1)
		self.assertRaises(ValueError, securityTransactionInterval, [""], 1)
		self.assertRaises(ValueError, securityTransactionInterval, -1, 1)
		self.assertRaises(ValueError, securityTransactionInterval, "aeae", 1)
