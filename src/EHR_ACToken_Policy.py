#!/usr/bin/env python3.5

'''
========================
EHR_ACToken_Policy module
========================
@TaskDescription: This module provide Capability token struct model and encapsulation of access control policy.
Module talks with db_layer and wrapper to evaluate token and AC policy
Used by server to evaluate whether to send EHR data or not
'''

import time
import datetime
import json
import sys
#from CapAC_Token import CapACToken
#from utilities import DatetimeUtil, TypesUtil, FileUtil
from flask import request

from EHR_ACToken_Proj import EHR_ACToken_Proj
from db_layer import *

now = datetime.datetime.now()
datestr=now.strftime("%Y-%m-%d")
timestr=now.strftime("%H:%M:%S")

#global variable
#contract_config = '../CapbilityToken/build/contracts/CapACToken.json'

httpProvider = 'http://localhost:8042'
contractAddr = EHR_ACToken_Proj.getAddress('EHR_ACToken_Proj', './addr_list.json')
contractConfig = '../contracts/build/contracts/EHR_ACToken_Proj.json'

#new global EHR_ACToken_Proj object (used to make transactions with SC)
mytoken = EHR_ACToken_Proj(httpProvider, contractAddr, contractConfig)

'''
EHR access control policy management
Server only uses this to check token AC, not to query token data directly
'''
class EHR_ACToken_Policy(object):

    # get token data from smart contract, return json fromat
    @staticmethod
    def get_token(tokenID):
        token_data = mytoken.queryTokenData(tokenID);
        json_token={}

        #Add token information
        json_token['name'] = token_data[0]
        json_token['gender'] = token_data[1]
        json_token['institutionAmount'] = token_data[2]
        json_token['authInstitutionNames'] = token_data[3]

        return json_token
    
    #could take these 3 functions out and call wrapper directly in WS_Server instead
    
    @staticmethod
    def add_institution(tokenId, institutionName, newInstitutionAddr):
        mytoken.addInstitution(tokenId, institutionName, newInstitutionAddr)
        
    @staticmethod
    def delete_institution(tokenId, institutionAddr):
        mytoken.deleteInstitution(tokenId, institutionAddr)
        
    @staticmethod
    def create_token(tokenId, institutionName, institutionAddr, patientName, patientGender):
        mytoken.createToken(tokenId, institutionName, institutionAddr, patientName, patientGender)

    # check token for institution using its address
    # should it check both SC and local db_layer? though, SC still has priority
    @staticmethod
    def check_token(tokenID, instrAddr):
        ret = False
        #time.sleep(2)
        ret = mytoken.checkToken(tokenID, instrAddr)
        #should fail if sender is not superInstitution (contract maker)
        #also if institution is not is AC list
        return ret
    
    #check db_layer for institution in registry table
    @staticmethod
    def check_institution_registry(institutionName, institutionAddress):
        ret = False
        path_db = 'REGD.db'
        reg_entry = RegistrationManager.select_ByName(path_db, institutionName)
        
        if len(reg_entry) < 1:
            return ret
        
        inst_address = reg_entry[0]['SC_Address']
        if institutionAddress == inst_address:
            ret = True
               
        return ret
        
    #check for institution in patient database    
    @staticmethod
    def check_patient_database(patientName, institutionAddress):
        ret = False
        path_db = 'PACD.db'
        patient_entry = PatientACManager.select_ByName(path_db, patientName)
        
        if len(patient_entry) < 1:
            return ret
        
        inst_addresses = patient_entry[0]['InstitutionAddress']
        splitAddresses = inst_addresses.split(",")
        if institutionAddress in splitAddresses:
            ret = True
               
        return ret
        
    #compare address input against super Institution address    
    @staticmethod    
    def check_address_json(address):
        ret = False
        superAddr = mytoken.getAddress('EHR_ACToken_Proj', './addr_list.json')
        if address == superAddr:
            ret = True
        
        return ret

def test_CapACToken():


    #Get account address
    accountAddr=CapACToken.getAddress('sam_miner_win7_0', '../CapbilityToken/test/addr_list.json')
    #print("Account: " + accountAddr)

    #Read token data using call
    #token_data=mytoken.getCapToken(accountAddr);
    #CapACToken.print_tokendata(token_data)
    #print(token_data)


    #token_data=CapPolicy.get_token(accountAddr)
    '''print(token_data['delegatee'][0])
    ac = TypesUtil.string_to_json(token_data['authorization'])
    print(ac['resource'])'''

    #FileUtil.AddLine('token.dat', TypesUtil.json_to_string(token_data))

    '''read_token=FileUtil.ReadLines('token.dat')
    json_token=TypesUtil.string_to_json(read_token[0])
    print(json_token['initialized'])'''

    #ret=CapPolicy.is_token_valid(token_data)

    #ret=CapPolicy.is_valid_access_request()
    

if __name__ == "__main__":

    #test_CapACToken()
    pass