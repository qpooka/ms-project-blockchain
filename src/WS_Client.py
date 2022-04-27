#!/usr/bin/env python3.5

'''
========================
WS_Client module
========================
@TaskDescription: This module provide encapsulation of client API that access to Web service.
Module makes request to server, to test server
'''
import time
import requests
import datetime
import json

#from EHR_ACToken_Proj import EHR_ACToken_Proj

import sys
#from utilities import DatetimeUtil, TypesUtil, FileUtil

now = datetime.datetime.now()
datestr=now.strftime("%Y-%m-%d")
timestr=now.strftime("%H:%M:%S")
    
class WSClient(object):
    
    #get a patient's EHR by tokenID? or by name?
    @staticmethod
    def Get_EHRbyTokenID(api_url, params, data_args={}):
        headers = {'Content-Type' : 'application/json'}
        response = requests.get(api_url, params = params, data = json.dumps(data_args), headers = headers)
        
        #wait for and then get response (in json)
        json_response = response.json()
        
        return json_response

    #get a patient's EHR by tokenID? or by name?
    @staticmethod
    def Get_TokenbyTokenID(api_url, params, data_args={}):
        headers = {'Content-Type' : 'application/json'}
        response = requests.get(api_url, params = params, data = json.dumps(data_args), headers = headers)
        
        #wait for and then get response (in json)
        json_response = response.json()
        
        return json_response
    
    #get patient's tokenID by Name
    @staticmethod
    def Get_TokenIdByName(api_url, params, data_args={}):
        headers = {'Content-Type' : 'application/json'}
        response = requests.get(api_url, params = params, data = json.dumps(data_args), headers = headers)
        
        #wait for and then get response (in json)
        json_response = response.json()
        
        return json_response
    
    #TODO: priority functions needed - 
    #   create : new registry entry, new patient entry+token,
    #   update : existing patient entry (add/delete institutions)
    #           when adding/deleting institutions from patient AC lists, don't need to delete from registry
    
    #lower priority functions - 
    #   delete : patient row, institution registry row, EHR row
    
    
    #create/post new patient entry/token into database and SC
    #SC call doesn't return anything
    #data input has name, gender, tokenID, institutionName, institutionAddress
    @staticmethod
    def Create_PatientEntry(api_url, data):
        headers = {'Content-Type' : 'application/json'}
        response = requests.post(api_url, data = json.dumps(data), headers = headers)
    
        json_response = response.json()      

        return json_response
        
    #create/post new institution into registry db
    #data input has name (of institution) and address
    @staticmethod
    def Create_InstitutionRegistryEntry(api_url, data):
        headers = {'Content-Type' : 'application/json'}
        response = requests.post(api_url, data = json.dumps(data), headers = headers)
    
        json_response = response.json()      

        return json_response
        
    #update/put - add institution into patient SC token, and local database?
    #data input has tokenID, institutionName, institutionAddress
    def Update_AddInstitution(api_url, data):
        headers = {'Content-Type' : 'application/json'}
        response = requests.put(api_url, data = json.dumps(data), headers = headers)
        
        json_response = response.json()      

        return json_response
    
    #update/put - delete institution from patient SC token, and local database?
    #data input has tokenID, institutionAddress
    def Update_DeleteInstitution(api_url, data):
        headers = {'Content-Type' : 'application/json'}
        response = requests.put(api_url, data = json.dumps(data), headers = headers)
        
        json_response = response.json()      

        return json_response
        
    
    '''
    Put id to delete data
    '''
    @staticmethod
    def Delete_Data(api_url, data):          
        headers = {'Content-Type' : 'application/json'}
        response = requests.delete(api_url, data=json.dumps(data), headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response

def test_get(data_args = {}):
    params = {}
    params['Name'] = data_args['Name']
    #print(params)
    
    #tokenID = WSClient.Get_TokenIdByName('http://128.226.78.89/test/api/v1.0/dt/TokenID', params, data_args)
    tokenEntry = WSClient.Get_TokenIdByName('http://0.0.0.0:1801/test/api/v1.0/dt/TokenID', params, data_args)
    tokenID = tokenEntry['TokenID']
    print(tokenID)
    params['TokenID'] = tokenID
    #print(WSClient.Get_EHRbyTokenID('http://128.226.78.89/test/api/v1.0/dt/EHR', params, data_args))
    EHR = WSClient.Get_EHRbyTokenID('http://0.0.0.0:1801/test/api/v1.0/dt/EHR', params, data_args)
    print(EHR)
    
    Token = WSClient.Get_TokenbyTokenID('http://0.0.0.0:1801/test/api/v1.0/dt/Token', params, data_args)
    print(Token)

def test_create_update_institution(data_args = {}):
    resp1 = WSClient.Create_InstitutionRegistryEntry('http://0.0.0.0:1801/test/api/v1.0/dt/create/inst_reg', data_args)
    resp2 = WSClient.Update_AddInstitution('http://0.0.0.0:1801/test/api/v1.0/dt/update/add/institution', data_args)
    print(resp1)
    print(resp2)
    print("Add Test finished")
    
def test_update_delete_institution(data_args = {}):
    resp1 = WSClient.Update_DeleteInstitution('http://0.0.0.0:1801/test/api/v1.0/dt/update/delete/institution', data_args)
    print(resp1)
    print("Delete Test finished")
    
def test_create_patient_entry(data_args = {}):
    resp = WSClient.Create_PatientEntry('http://0.0.0.0:1801/test/api/v1.0/dt/create/patient_entry', data_args)
    print(resp)
    
def test_add(data_args={}):
    project = {
        'title': 'post_new',
        'description': 'post_description',
        'date': datestr,
        'time': timestr
    }
    project_data = {'project_data':project}
    
    if(bool(data_args)):
        project_data['token_data']=data_args['token_data']
    json_response=WSClient.Create_Data('http://128.226.78.217/test/api/v1.0/dt/create',project_data)
    #print(json_response['project_data'])
    print(json_response)
    

    
def test_EHR_ACToken():
    
    #params = {'project_id':'2'}
    data_args = {'project_id':'2'}
    
    start_time=time.time()
    
    #print token_data   
    #test_add(data_args)
    #test_update(data_args)
    #test_delete(data_args) 
    test_search(data_args)
    
    end_time=time.time()
    exec_time=end_time-start_time
    
    time_exec=format(exec_time*1000, '.3f')
    print("Execution time is:%2.6f" %(exec_time))

    #FileUtil.AddLine('exec_time_client.log', time_exec)
    '''print WSClient.Get_Datasets('http://128.226.78.217/test/api/v1.0/dt', data_args)
    print WSClient.Get_DataByID('http://128.226.78.217/test/api/v1.0/dt/project',params, data_args)'''

if __name__ == "__main__":
    #get test (get Jeff token and EHR)
    data_args = {'Name' : 'Bob', 'InstitutionName' : 'EHR_ACToken_Proj', \
                    'InstitutionAddress' : '0x548bdfcaeb2758ee2a8ca71d8f5baafacf5ea49f'}
    test_get(data_args)
    
    #add institution test (add differentInst to Jeff token)
    '''params = {}
    params['Name'] = 'Jeff'
    data_args = {'Name' : 'Jeff', 'SuperAddress' : '0x548bdfcaeb2758ee2a8ca71d8f5baafacf5ea49f', \
                   'NewInstitutionName' : 'differentInst', \
                    'NewAddress' : '0x6e8df907de0c1bb5a6d32a21ff0042fbef0c05d0'}
    tokenEntry = WSClient.Get_TokenIdByName('http://0.0.0.0:1801/test/api/v1.0/dt/TokenID', params, data_args)
    tokenID = tokenEntry['TokenID']
    
    data_args['TokenID'] = str(tokenID)
    
    test_create_update_institution(data_args)'''
    
    #delete institution test (delete newInst from token AC list Jeff)
    '''params = {}
    params['Name'] = 'Jeff'
    data_args = {'Name' : 'Jeff', 'SuperAddress' : '0x548bdfcaeb2758ee2a8ca71d8f5baafacf5ea49f', \
                   'NewInstitutionName' : 'newInst', \
                    'NewAddress' : '0xa7d094a545a59610a9ef9f36afb4d640d3140cd6'}
    tokenEntry = WSClient.Get_TokenIdByName('http://0.0.0.0:1801/test/api/v1.0/dt/TokenID', params, data_args)
    tokenID = tokenEntry['TokenID']
    
    data_args['TokenID'] = str(tokenID)
    test_update_delete_institution(data_args)'''
    
    #create new token in SC and new entry in database
    '''data_args = {'Name' : 'Bob', 'Gender' : 'Male', 'TokenID' : '0x1111dfcaeb2758ee2a8ca71d8f5baafacf5ea49f', \
                    'NewInstitutionName' : 'EHR_ACToken_Proj', 'NewAddress' : '0x548bdfcaeb2758ee2a8ca71d8f5baafacf5ea49f', \
                    'SuperAddress' : '0x548bdfcaeb2758ee2a8ca71d8f5baafacf5ea49f'}
    test_create_patient_entry(data_args)'''
    
    #why id the EHR that is returned all jumboed up in order?
    #test_EHR_ACToken()
    pass