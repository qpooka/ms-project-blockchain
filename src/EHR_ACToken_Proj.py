#!/usr/bin/env python3.5

'''
========================
Access control token module
========================
@author: Jeffrey Cheuk
@Email:  jcheuk1@binghamton.edu
@TaskDescription: This module provide encapsulation of web3.py API to interact with EHR_ACToken_Proj.sol smart contract.
'''

from web3 import Web3, HTTPProvider, IPCProvider
from utilities import DatetimeUtil, TypesUtil
import json, datetime, time

class EHR_ACToken_Proj(object):
	def __init__(self, http_provider, contract_addr, contract_config):
		# configuration initialization
		self.web3 = Web3(HTTPProvider(http_provider))
		self.contract_address = Web3.toChecksumAddress(contract_addr)
		self.contract_config = json.load(open(contract_config))

		# new contract object
		self.contract = self.web3.eth.contract()
		self.contract.address = self.contract_address
		self.contract.abi = self.contract_config['abi']


	# return accounts address
	def getAccounts(self):
		return self.web3.eth.accounts

	# return accounts balance
	def getBalance(self, account_addr=''):
		if(account_addr == ''):
			# get accounts[0] balance
			checksumAddr = self.web3.eth.coinbase
		else:
			#Change account address to EIP checksum format
			checksumAddr = Web3.toChecksumAddress(account_addr)	
		return self.web3.fromWei(self.web3.eth.getBalance(checksumAddr), 'ether')

	'''
	Call a contract function, executing the transaction locally using the eth_call API. 
	This will not create a new public transaction.
	'''
	# get all data from a token
	def queryTokenData(self, tokenAddress):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(tokenAddress)

		# get token status
		tokenData = self.contract.call({'from': self.web3.eth.coinbase}).queryTokenData(checksumAddr)
		return tokenData

	# add institution to a token's access list
	def addInstitution(self, tokenAddress, newInstName, newInstAddress):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(tokenAddress)
        newInstAddr = Web3.toChecksumAddress(newInstAddress)

		# Execute the specified function by sending a new public transaction.
		ret = self.contract.transact({'from': self.web3.eth.coinbase}).addInstitution(checksumAddr, newInstName, newInstAddr)

	# delete institution from a token's access list
	def deleteInstitution(self, tokenAddress, instAddress):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(tokenAddress)
        checksumInstAddr = Web3.toChecksumAddress(instAddress)	

		# Execute the specified function by sending a new public transaction.	
		ret = self.contract.transact({'from': self.web3.eth.coinbase}).deleteInstitution(checksumAddr, checksumInstAddr)

	# create token and return token address
	def createToken(self, institutionName, patientName, patientGender):
		#Change account address to EIP checksum format
		#checksumAddr = Web3.toChecksumAddress(account_addr)	

		# Execute the specified function by sending a new public transaction.	
		ret = self.contract.transact({'from': self.web3.eth.coinbase}).createToken(institutionName, patientName, patientGender)
        return ret

	# check token for institution, return true or false
    # only super institution (contract creator) can check for institution other than itself
	def checkToken(self, tokenAddress, institutionAddress):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(tokenAddress)	
        checksumInstAddr = Web3.toChecksumAddress(institutionAddress)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).checkToken(checksumAddr, checksumInstAddr)
        return ret

	# Print token date, helper function
	@staticmethod
	def print_tokendata(tokenStatus):
		#print token status
		for i in range(0,len(tokenStatus)):
			if(i == 4 or i == 5):
                print(tokenStatus[i])
				# dt=DatetimeUtil.timestamp_datetime(tokenStatus[i])
				#dt=datetime.datetime.utcfromtimestamp(token_data[i]/1e3)
				# print(DatetimeUtil.datetime_string(dt))
				#print(DatetimeUtil.datetime_timestamp(dt))
				#print(token_data[i])
			else:
				print(tokenStatus[i])

	# get address from json file, helper function
	@staticmethod
	def getAddress(node_name, datafile):
		address_json = json.load(open(datafile))
		return address_json[node_name]


if __name__ == "__main__":
	#http_provider = 'http://localhost:8042'
	#contract_addr = PatientACToken.getAddress('PatientACToken', './addr_list.json')
	#contract_config = '../contracts/build/contracts/PatientACToken.json'

    httpProvider = 'http://localhost:8042'
    contractAddr = EHR_ACToken_Proj.getAddress('EHR_ACToken_Proj', './addr_list.json')
    contractConfig = '../contracts/build/contracts/EHR_ACToken_Proj.json'

	#new PatientACToken object
	myEHR_ACToken_Proj = EHR_ACToken_Proj(httpProvider, contractAddr, contractConfig)


	#------------------------- test contract API ---------------------------------
	#getAccounts
	accounts = myEHR_ACToken_Proj.getAccounts()
	balance = myEHR_ACToken_Proj.getBalance(accounts[0])
	print("Host accounts: %s" %(accounts))
	print("coinbase balance:%d" %(balance))
	print("--------------------------------------------------------------------")

    #address for contract?
    #address for token is generated by smart contract, so save it in variable

	user_address = PatientACToken.getAddress('sam_ubuntu', './addr_list.json')
	patientACToken_address = PatientACToken.getAddress('PatientACToken', './addr_list.json')

	# list Access control
	'''json_data=TypesUtil.string_to_json(token_data[-1])
	print("resource: %s" %(json_data['resource']))
	print("action: %s" %(json_data['action']))
	print("conditions: %s" %(json_data['conditions']))'''
    
    #structure:
    #as the super Instituion:
    
    #create token, saving token address in variable (to use for below instructions)
    #tokenAddress1 = createToken(__, __, __)
    #print(tokenAddress1)
    
    #query token data (and print it)
    #token1DataInitial = queryTokenData(tokenAddress1)
    #print_tokendata(token1DataInitial)
    
    #add institutions (other than initial one)
    #addInstitution(tokenAddress1, ___)
    
    #check token for institutions
    #checkToken(tokenAddress1, __)
    
    #query token data (and print it)
    #token1DataAdd = queryTokenData(tokenAddress1)
    #print_tokendata(token1DataAdd)
    
    #delete institutions (other than initial one)
    #deleteInstitution(tokenAddress1, __)
    
    #check token for institutions
    #checkToken(tokenAddress1, __)
    
    #query token data (and print it)
    #token1DataDelete = queryTokenData(tokenAddress1)
    #print_tokendata(token1DataDelete)
    

	pass