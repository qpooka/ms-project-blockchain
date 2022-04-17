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

now = datetime.datetime.now()
datestr=now.strftime("%Y-%m-%d")
timestr=now.strftime("%H:%M:%S")

#global variable
#contract_config = '../CapbilityToken/build/contracts/CapACToken.json'

httpProvider = 'http://localhost:8042'
contractAddr = EHR_ACToken_Proj.getAddress('EHR_ACToken_Proj', './addr_list.json')
contractConfig = '../contracts/build/contracts/EHR_ACToken_Proj.json'

#new global EHR_ACToken_Proj object (used to make transactions with SC)
mytoken = EHR_ACToken_Proj(http_provider, contract_addr, contract_config)

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

    # check token for institution using its address
    # should it check both SC and local db_layer? though, SC still has priority
    @staticmethod
    def check_token(tokenID, instrAddr):
        ret = mytoken.checkToken(tokenID, instrAddr)
        return ret
    
    #check db_layer for institution in registry table
    def check_institution_registry(institutionName):
        ret = False
        path_db = ''
        reg_entry = RegistrationManager.select_ByName()
        if institutionName in reg_entry:
            ret = True
            
        return ret
        

	# check token status, like status flag, issue and expire time.
	@staticmethod
	def is_token_valid(token_data):
		ret = True
		#check enable flag
		if( token_data['initialized']!=True or token_data['isValid']!=True):
			ret = False

		#check issue time and expire time
		now_stamp = DatetimeUtil.datetime_timestamp(datetime.datetime.now())
		if( (token_data['issuedate'] > now_stamp) or (now_stamp > token_data['expireddate']) ):
			ret = False
		return ret

	# verify acccess right
	@staticmethod
	def is_access_valid(token_data, acess_args=''):
		ret = True

		#token_authorization = token_data[2][1]
		ac_data=TypesUtil.string_to_json(token_data['authorization'])
		#print(ac_data)

		if(ac_data['action']!=acess_args['method'] or 
			ac_data['resource']!=str(acess_args['url_rule']) or 
			not CapPolicy.is_condition_valid(ac_data['conditions'])):
			'''print(ac_data['action']!=acess_args['method'])
			print(ac_data['resource']==str(acess_args['url_rule']))
			print(CapPolicy.is_condition_valid(ac_data['conditions']))'''
			ret = False
		return ret

	# check condition status to verify context requirement
	@staticmethod
	def is_condition_valid(condition_data):
		if(condition_data==[]):
			return True
		#handle Timespan
		if(condition_data['type']=='Timespan'):
			#print condition_data['value']['start']
			starttime = DatetimeUtil.string_datetime(condition_data['value']['start'], "%H:%M:%S")
			endtime = DatetimeUtil.string_datetime(condition_data['value']['end'], "%H:%M:%S")
			nowtime=DatetimeUtil.string_datetime(timestr, "%H:%M:%S")
			'''print(starttime)
			print(endtime)
			print(nowtime)'''
			#check if timespan condition is valid
			if(not (starttime<nowtime<endtime) ):
				print("condition validation fail!")
				return False
		return True

	'''
	Valid access request based on policy, call by interposing service API
	'''	
	@staticmethod	
	def is_valid_access_request(req_args):
		#Get account address
		accountAddr=CapACToken.getAddress('sam_miner_win7_0', '../CapbilityToken/test/addr_list.json')

		#Define ls_time_exec to save executing time to log
		ls_time_exec=[]

		#get token data
		start_time=time.time()

		# 1) get token from smart contract, high overload
		token_data=CapPolicy.get_token(accountAddr)

		# 2) Save token data to local token.dat
		#FileUtil.AddLine('token.dat', TypesUtil.json_to_string(token_data))

		# 3) read token from local data, low overload
		'''read_token=FileUtil.ReadLines('token.dat')
		token_data=TypesUtil.string_to_json(read_token[0])'''
		#print(token_data)

		exec_time=time.time()-start_time
		ls_time_exec.append(format(exec_time*1000, '.3f'))	
		print("Execution time of get_token is:%2.6f" %(exec_time))

		#extract access action from request
		access_data={}
		access_data['url_rule']=req_args.url_rule
		access_data['method']=req_args.method
		#print(access_data)

		start_time=time.time()
		if(not CapPolicy.is_token_valid(token_data)):
			print('token valid fail')
			return False
		exec_time=time.time()-start_time
		ls_time_exec.append(format(exec_time*1000, '.3f'))	
		print("Execution time of is_token_valid is:%2.6f" %(exec_time))

		start_time=time.time()
		if(not CapPolicy.is_access_valid(token_data, access_data)):
			print('access valid fail')
			return False
		exec_time=time.time()-start_time
		ls_time_exec.append(format(exec_time*1000, '.3f'))		
		print("Execution time of is_access_valid is:%2.6f" %(exec_time))

		#transfer list to string
		str_time_exec=" ".join(ls_time_exec)
		#print(str_time_exec)
		FileUtil.AddLine('exec_time_server.log', str_time_exec)

		return True

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

	test_CapACToken()
	pass