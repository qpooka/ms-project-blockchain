#!/usr/bin/env python3.5

'''
========================
WS_Server module
========================
@TaskDescription: This module provide encapsulation of server API that handle and response client's request.
Module handles client requests, makes calls to db_layer and EHR_ACToken_Policy to return dummy data
'''

import datetime
import json
from flask import Flask, jsonify
from flask import abort,make_response,request

from db_layer import *
from EHR_ACToken_Proj import EHR_ACToken_Proj
from EHR_ACToken_Policy import EHR_ACToken_Policy

app = Flask(__name__)

now = datetime.datetime.now()
datestr=now.strftime("%Y-%m-%d")
timestr=now.strftime("%H:%M:%S")

#Defining dictionary dataset model
projects = [
    {
        'id': 1,
        'title':u'test',
        'description':u'Hello World',
        'date':u'04-28-2017',
        'time': u'Morning'
    },
    {
        'id': 2,
        'title':u'GET',
        'description':u'test GET APIs',
        'date':u'4-29-2017',
        'time': u'12:00 am'
    }
]

#========================================== Error handler ===============================================
#Error handler for abort(404) 
@app.errorhandler(404)
def not_found(error):
    #return make_response(jsonify({'error': 'Not found'}), 404)
    response = jsonify({'result': 'Failed', 'message':  error.description['message']})
    response.status_code = 404
    return response

#Error handler for abort(400) 
@app.errorhandler(400)
def type_error(error):
    #return make_response(jsonify({'error': 'type error'}), 400)
    response = jsonify({'result': 'Failed', 'message':  error.description['message']})
    response.status_code = 400
    return response
    
#Error handler for abort(401) 
@app.errorhandler(401)
def access_deny(error):
    response = jsonify({'result': 'Failed', 'message':  error.description['message']})
    response.status_code = 401
    return response

    
#========================================== Request handler ===============================================
#for all operations, could check:
#extra input (institution address)
#that will be checked against PatientACManager database and json file 

#GET req
@app.route('/test/api/v1.0/dt/EHR', methods=['GET'])
def get_EHRbyTokenID():
    #missing, deny access
    req_data = json.loads(request.data)
    if (req_data.get('InstitutionName') == None) or (req_data.get('InstitutionAddress') == None) or (req_data.get('Name') == None):
       abort(401, {'message': 'missing relevant information, deny access'})
    
    tokenID = request.args.get('TokenID', default = 1, type = str)
    
    #authorization, check SC and inst registry
    #need tokenID and institution address
    
    if(not EHR_ACToken_Policy.check_institution_registry(req_data['InstitutionName'], req_data['InstitutionAddress'])):
        abort(401, {'message2': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_patient_database(req_data['Name'], req_data['InstitutionAddress'])):
        abort(401, {'message': 'Authorization fail, deny access'})
    
    #check SC
    if(not EHR_ACToken_Policy.check_token(str(tokenID), req_data['InstitutionAddress'])):
        abort(401, {'message': 'Authorization fail, deny access'})
    
    
    print("========HERE IS IT=========")
    print("PASSED TEST")
    print("========ENDS HERE==========")
    
    
    #call SC to query token (based on tokenID), extract name
    #also check token, the institution name matches
    aToken = EHR_ACToken_Policy.get_token(str(tokenID))
    print(aToken)
    print(RegistrationManager.select_Allentry('REGD.db'))
    
    patientName = aToken['name']
    
    try:
        patientEHR = EHR_Manager.select_ByName('EHRD.db', patientName)
        EHRret = patientEHR[0]
    except:
        abort(404, {'message': 'No EHR found'})
        
    return jsonify(EHRret), 201
    

'''    
#GET req
@app.route('/test/api/v1.0/dt/All/Tokens', methods=['GET'])
def get_AllTokens():  
    patientEntries = PatientACManager.select_Allentry('PACD.db')
    return jsonify({'entries' : patientEntries}), 201
'''

#get from SC  
#GET req
@app.route('/test/api/v1.0/dt/Token', methods=['GET'])  
def get_TokenByTokenID():    
    #missing, deny access
    req_data = json.loads(request.data)
    if (req_data.get('InstitutionName') == None) or (req_data.get('InstitutionAddress') == None) or (req_data.get('Name') == None):
       abort(401, {'message': 'missing relevant information, deny access'})
    
    tokenID = request.args.get('TokenID', default = 1, type = str)
    
    #authorization, check SC and inst registry
    #need tokenID and institution address
    
    if(not EHR_ACToken_Policy.check_institution_registry(req_data['InstitutionName'], req_data['InstitutionAddress'])):
        abort(401, {'message2': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_patient_database(req_data['Name'], req_data['InstitutionAddress'])):
        abort(401, {'message': 'Authorization fail, deny access'})
    
    #check SC
    if(not EHR_ACToken_Policy.check_token(str(tokenID), req_data['InstitutionAddress'])):
        abort(401, {'message': 'Authorization fail, deny access'})

    aToken = EHR_ACToken_Policy.get_token(str(tokenID))
    
    return jsonify(aToken), 201
    
#GET req
@app.route('/test/api/v1.0/dt/TokenID', methods=['GET'])
def get_TokenIdByName():
    #missing, deny access
    req_data = json.loads(request.data)
    if (req_data.get('InstitutionName') == None) or (req_data.get('InstitutionAddress') == None):
       abort(401, {'message': 'missing relevant information, deny access'})
    
    patientName = request.args.get('Name', default = 1, type = str)
    
    if(not EHR_ACToken_Policy.check_institution_registry(req_data['InstitutionName'], req_data['InstitutionAddress'])):
        abort(401, {'message2': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_patient_database(patientName, req_data['InstitutionAddress'])):
        abort(401, {'message': 'Authorization fail, deny access'})
    
    patientEntry = PatientACManager.select_ByName('PACD.db', patientName)
    tokenID = patientEntry[0]['TokenID']
    
    #get tokenID from local database
    
    return jsonify({'TokenID' : tokenID}), 201
    
#POST req
@app.route('/test/api/v1.0/dt/create/patient_entry', methods=['POST'])
def create_patient_entry():
    #Token missing, deny access
    req_data = json.loads(request.data)
    if ('Name' not in req_data) or ('TokenID' not in req_data) \
        or ('NewInstitutionName' not in req_data) or ('NewAddress' not in req_data) \
        or ('SuperAddress' not in req_data) or ('Gender' not in req_data):
        abort(401, {'message': 'missing relevant information, deny access'})
    
    if not request.json:
        abort(400, {'message': 'No data in parameter for operation.'})
    
    if(not EHR_ACToken_Policy.check_address_json(req_data['SuperAddress'])):
        abort(401, {'message': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_institution_registry(req_data['NewInstitutionName'], req_data['NewAddress'])):
        abort(401, {'message2': 'Authorization fail, deny access'})
    
    data_in = [req_data['Name'], req_data['TokenID'], req_data['NewInstitutionName'], req_data['NewAddress']]
    
    #call db to add patient entry into PACD database, insert data as a list
    PatientACManager.insert_entry('PACD.db', data_in)
    
    #call SC to add patient token
    EHR_ACToken_Policy.create_token(req_data['TokenID'], req_data['NewInstitutionName'], req_data['NewAddress'], req_data['Name'], req_data['Gender'])
    
    #return jsonify({'project_data': project}), 201
    return jsonify({'result': 'Succeed', 'data_in_SC': data_in}), 201    
    
#POST req
@app.route('/test/api/v1.0/dt/create/inst_reg', methods=['POST'])
def create_institution_registry():
    #missing, deny access
    req_data = json.loads(request.data)
    if ('Name' not in req_data) or ('NewAddress' not in req_data) \
        or ('SuperAddress' not in req_data) or ('NewInstitutionName' not in req_data):
        abort(401, {'message': 'missing relevant information, deny access'})
    
    #what authorization to include? this wouldn't involve SC
    
    #Authorization process 
    if not request.json:
        abort(400, {'message': 'No data in parameter for operation.'})

    if(not EHR_ACToken_Policy.check_address_json(req_data['SuperAddress'])):
        abort(401, {'message': 'Authorization fail, deny access'})
    
    data_in = [req_data['NewInstitutionName'], req_data['NewAddress']]
    
    #call to db_layer to add entry into REGD.db database
    RegistrationManager.insert_entry('REGD.db', data_in)
    
    return jsonify({'result': 'Succeed', 'data' : data_in}), 201     

    #adding//deleting institutions will need auth that:
    #   checks for existing insitution in PatientACManager database
    #   this will require extra input that won't be used in SC input

@app.route('/test/api/v1.0/dt/update/add/institution', methods=['PUT'])
def update_add_institution():
    #data needed: Name, institutionAddess, institutionName, tokenID, superInstitution address
    #putting everything in data_args, no params
    
    #missing, deny access
    req_data = json.loads(request.data)
    if ('Name' not in req_data) or ('SuperAddress' not in req_data) \
        or ('TokenID' not in req_data) or ('NewAddress' not in req_data) \
        or ('NewInstitutionName' not in req_data):
        abort(401, {'message': 'missing relevant information, deny access'})
    
    if(not EHR_ACToken_Policy.check_address_json(req_data['SuperAddress'])):
        abort(401, {'message1': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_institution_registry(req_data['NewInstitutionName'], req_data['NewAddress'])):
        abort(401, {'message2': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_patient_database(req_data['Name'], req_data['SuperAddress'])):
        abort(401, {'message3': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_token(str(req_data['TokenID']), req_data['SuperAddress'])):
        abort(401, {'message4': 'Authorization fail, deny access'})
    
    data_in = [req_data['Name'], req_data['NewInstitutionName'], req_data['NewAddress']]
    
    PatientACManager.update_addInstitution('PACD.db', data_in)
    #call SC to update AC list in token
    #maybe do this in EHR_ACToken_Policy? or directly in WS_Server?
    EHR_ACToken_Policy.add_institution(req_data['TokenID'], req_data['NewInstitutionName'], req_data['NewAddress'])
    
    return jsonify({'result': 'Succeed', 'data' : data_in}), 201     
    
#delete institution needs: Name, tokenID, institutionAddress, superInstitution address
@app.route('/test/api/v1.0/dt/update/delete/institution', methods=['PUT'])
def update_delete_institution():
    #missing, deny access
    print(RegistrationManager.select_Allentry('REGD.db'))
    
    req_data = json.loads(request.data)
    if ('Name' not in req_data) or ('SuperAddress' not in req_data) \
        or ('TokenID' not in req_data) or ('NewAddress' not in req_data) \
        or ('NewInstitutionName' not in req_data):
        abort(401, {'message': 'missing relevant information, deny access'})
    
    if(not EHR_ACToken_Policy.check_address_json(req_data['SuperAddress'])):
        abort(401, {'message1': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_institution_registry(req_data['NewInstitutionName'], req_data['NewAddress'])):
        abort(401, {'message2': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_patient_database(req_data['Name'], req_data['SuperAddress'])):
        abort(401, {'message3': 'Authorization fail, deny access'})
    
    if(not EHR_ACToken_Policy.check_token(str(req_data['TokenID']), req_data['SuperAddress'])):
        abort(401, {'message4': 'Authorization fail, deny access'})
    
    data_in = [req_data['Name'], req_data['NewInstitutionName'], req_data['NewAddress']]
    
    PatientACManager.update_deleteInstitution('PACD.db', data_in)
    #call SC to update AC list in token
    #maybe do this in EHR_ACToken_Policy? or directly in WS_Server?
    EHR_ACToken_Policy.delete_institution(req_data['TokenID'], req_data['NewAddress'])
    
    return jsonify({'result': 'Succeed', 'data' : data_in}), 201    
    
#=====================================================

   
#POST req. add title,description , date-time will be taken current fron system. id will be +1
@app.route('/test/api/v1.0/dt/create', methods=['POST'])
def create_project():
    #Token missing, deny access
    req_data=json.loads(request.data)
    if('token_data' not in req_data):
        abort(401, {'message': 'Token missing, deny access'})
    
    #Authorization process
    '''if(not CapPolicy.is_valid_access_request(request)):
        abort(401, {'message': 'Authorization fail, deny access'})'''
        
    if not request.json:
        abort(400, {'message': 'No data in parameter for operation.'})

    proj_json=req_data['project_data']
    project = {
        'id': projects[-1]['id'] + 1,
        'title': proj_json['title'],
        'description': proj_json['description'],
        'date': proj_json['date'],
        'time': proj_json['time']
    }
    projects.append(project)
    #return jsonify({'project_data': project}), 201
    return jsonify({'result': 'Succeed'}), 201

#PUT req. Update any paraments by id number.
@app.route('/test/api/v1.0/dt/update', methods=['PUT'])
def update_project():
    #Token missing, deny access
    req_data=json.loads(request.data)
    if('token_data' not in req_data):
        abort(401, {'message': 'Token missing, deny access'})
    
    #Authorization process
    '''if(not CapPolicy.is_valid_access_request(request)):
        abort(401, {'message': 'Authorization fail, deny access'})'''
        
    if not request.json:
        abort(400, {'message': 'No data in parameter for operation.'})
        
    #get json data
    proj_json=req_data['project_data']
    
    #get updating record id
    project_id=proj_json['id']
    
    #get record based on id
    project = [project for project in projects if project['id'] == project_id]
    
    #data verification
    if len(project) == 0:
        abort(404, {'message': 'No data found'})
    if not request.json:
        abort(400, {'message': 'Not JSON or data of title is not unicode.'})
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400, {'message': 'Not JSON or data of description is not unicode.'})
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400, {'message': 'Not JSON or data of date is not unicode.'})
    if 'date' in request.json and type(request.json['date']) is not unicode:
        abort(400, {'message': 'Not JSON or data of time is not unicode.'})
    if 'time' in request.json and type(request.json['time']) is not unicode:
        abort(400, {'message': 'Not JSON or data of title is not unicode.'})
        
    #update data field
    project[0]['title'] = proj_json['title']
    project[0]['description'] = proj_json['description']
    project[0]['date'] = proj_json['date']
    project[0]['time'] = proj_json['time']
    
    #return jsonify({'project_data': project}), 201
    return jsonify({'result': 'Succeed'}), 201
    
#DELETE req. Delete by id number.
@app.route('/test/api/v1.0/dt/delete', methods=['DELETE'])
def delete_project():
    #Token missing, deny access
    req_data=json.loads(request.data)
    if('token_data' not in req_data):
        abort(401, {'message': 'Token missing, deny access'})
    
    #Authorization process
    '''if(not CapPolicy.is_valid_access_request(request)):
        abort(401, {'message': 'Authorization fail, deny access'})'''
        
    if not request.json:
        abort(400, {'message': 'No data in parameter for operation.'})
        
    #get json data
    #req_json=request.json

    #get updating record id
    project_id=req_data['id']

    #get record based on id
    project = [project for project in projects if project['id'] == project_id]

    if len(project) == 0:
        abort(404, {'message': 'No data found'})
    projects.remove(project[0])
    return jsonify({'result': 'Succeed'}), 201
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1801, debug=True)