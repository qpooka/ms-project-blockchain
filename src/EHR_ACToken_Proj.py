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
import json, datetime, time
import sys
import argparse

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
        
    def getBalance(self, account_addr = ''):
        if(account_addr == ''):
            checksumAddr = self.web3.eth.coinbase
        else:
            checksumAddr = Web3.toChecksumAddress(account_addr)
        return self.web3.fromWei(self.web3.eth.getBalance(checksumAddr), 'ether')

    '''
    Call a contract function, executing the transaction locally using the eth_call API. 
    This will not create a new public transaction.
    '''
    
    # get all data from a token
    def queryTokenData(self, tokenId):
        #Change account address to EIP checksum format
        # checksumAddr = Web3.toChecksumAddress(tokenAddress)

        # get token status
        tokenData = self.contract.call({'from': self.web3.eth.coinbase}).queryTokenData(tokenId)
        # tokenData = self.contract.functions.queryTokenData(checksumAddr).call({'from': self.web3.eth.coinbase})
        return tokenData

    # create token and return token address
    def createToken(self, tokenId, institutionName, institutionAddr, patientName, patientGender):
        #Change account address to EIP checksum format
        #checksumAddr = Web3.toChecksumAddress(account_addr)
        
        # Execute the specified function by sending a new public transaction.   
        ret = self.contract.transact({'from': self.web3.eth.coinbase}).createToken(tokenId, institutionName, institutionAddr, patientName, patientGender)
        return ret
        
    # addresses are inputed as string    
    def addInstitution(self, tokenId, institutionName, newInstitutionAddr):
        ret = self.contract.transact({'from': self.web3.eth.coinbase}).addInstitution(tokenId, institutionName, newInstitutionAddr)
        return ret
    
    def deleteInstitution(self, tokenId, instAddr):
        ret = self.contract.transact({'from': self.web3.eth.coinbase}).deleteInstitution(tokenId, instAddr)
        return ret
        
    def checkToken(self, tokenId, instrAddr):
        retval = self.contract.call({'from': self.web3.eth.coinbase}).checkToken(tokenId, instrAddr)
        return retval
        
    # Print token date, helper function
    @staticmethod
    def print_tokendata(tokenStatus):
        #print token status
        for i in range(0,len(tokenStatus)):
            if(i == 3):
                tokenString = str(tokenStatus[i])
                print(tokenString.split(','))
                #dt=DatetimeUtil.timestamp_datetime(tokenStatus[i])
                #dt=datetime.datetime.utcfromtimestamp(token_data[i]/1e3)
                #print(DatetimeUtil.datetime_string(dt))
                #print(DatetimeUtil.datetime_timestamp(dt))
                #print(token_data[i])
            else:
                print(tokenStatus[i])

    # get address from json file, helper function
    @staticmethod
    def getAddress(node_name, datafile):
        address_json = json.load(open(datafile))
        return address_json[node_name]

def define_and_get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run test evaulation app."
    )
    parser.add_argument("--test_op", type=int, default=0, 
                        help="Execute test operation: \
                        0-contract information, \
                        1-queryTokenData, \
                        2-createToken, \
                        3-checkToken, \
                        4-addInstitution, \
                        5-deleteInstitution")

    parser.add_argument("--tokenid", type=str, default="00", 
                        help="input token id")
                        
    #parser.add_argument("--instAddr", type=str, default="00", help="input inst address")

    args = parser.parse_args(args=args)
    return args

if __name__ == "__main__":

    args = define_and_get_arguments()

    httpProvider = 'http://localhost:8042'
    contractAddr = EHR_ACToken_Proj.getAddress('EHR_ACToken_Proj', './addr_list.json')
    contractConfig = '../contracts/build/contracts/EHR_ACToken_Proj.json'

    #new object
    myEHR_ACToken_Proj = EHR_ACToken_Proj(httpProvider, contractAddr, contractConfig)

    newInstAddr = EHR_ACToken_Proj.getAddress('newInst', './addr_list.json')
    diffInstAddr = EHR_ACToken_Proj.getAddress('differentInst', './addr_list.json')

    tokenID = args.tokenid
    #instADDR = args.instAddr
    
    if(args.test_op==1):
        #--------------- show nodes latency curves--------------------
        tokenData = myEHR_ACToken_Proj.queryTokenData(tokenID)
        EHR_ACToken_Proj.print_tokendata(tokenData)
        
    elif(args.test_op==2):
        #--------------- create token data given id --------------------
        patient1Name = 'Alice'
        patient1Gender = 'female'
        myEHR_ACToken_Proj.createToken(tokenID, 'EHR_ACToken_Proj', contractAddr, patient1Name, patient1Gender)
        
    elif(args.test_op == 3):
        #check token for institutions
        tokenExist1 = bool(myEHR_ACToken_Proj.checkToken(tokenID, contractAddr))
        if tokenExist1 == True:
            print("Yes, super institution is in AC list")
        else:
            print("Not in AC list")
        
        tokenExist2 = (myEHR_ACToken_Proj.checkToken(tokenID, newInstAddr))
        if tokenExist2 == True:
            print("Yes, newInst is in AC list")
        else:
            print("Not in AC list")
            
        tokenExist3 = (myEHR_ACToken_Proj.checkToken(tokenID, diffInstAddr))
        if tokenExist3 == True:
            print("Yes, differentInst is in AC list")
        else:
            print("Not in AC list")
        
        
    elif(args.test_op == 4):
        #add institutions
        myEHR_ACToken_Proj.addInstitution(tokenID, "newInst", newInstAddr)
        #myEHR_ACToken_Proj.addInstitution(tokenID, "differentInst", diffInstAddr)
        
    elif(args.test_op == 5):
        #delete institutions
        #myEHR_ACToken_Proj.deleteInstitution(tokenID, newInstAddr)
        myEHR_ACToken_Proj.deleteInstitution(tokenID, diffInstAddr)
        
    else:
        #------------------------- show contract information --------------------------------
        #getAccounts
        accounts = myEHR_ACToken_Proj.getAccounts()
        balance = myEHR_ACToken_Proj.getBalance(accounts[0])
        print("Host accounts: %s" %(accounts))
        print("coinbase balance:%d" %(balance))
