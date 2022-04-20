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
#from BlendCapAC_Policy import CapPolicy
#from RBAC_Policy import RBACPolicy
#from ABAC_Policy import ABACPolicy

from db_layer import *
from EHR_ACToken_Proj import EHR_ACToken_Proj

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
#GET req
@app.route('/test/api/v1.0/dt/EHR', methods=['GET'])
def get_EHRbyTokenID():
    #Token missing, deny access
	#if(request.data=='{}'):
	#	abort(401, {'message': 'Token missing, deny access'})
    
    #authorization, check SC
    
    tokenID = request.args.get('TokenID', default = 1, type = str)
    
    #call SC to query token (based on tokenID), extract name
    
    patientName = 
    
    patientEHR = EHR_Manager.select_ByName('EHRD.db', patientName)
    EHRret = patientEHR[0]
    return jsonify(EHRret), 201
    
    return 
    
#GET req
@app.route('/test/api/v1.0/dt/All/Tokens', methods=['GET'])
def get_AllTokens():  
    patientEntries = PatientACManager.select_Allentry('PACD.db')
    return jsonify({'entries' : patientEntries}), 201
    
#GET req
@app.route('/test/api/v1.0/dt/TokenID', methods=['GET'])
def get_TokenIdByName():
    #Token missing, deny access
	#if(request.data=='{}'):
	#	abort(401, {'message': 'Token missing, deny access'})
    
    
    
    patientName = request.args.get('Name', default = 1, type = str)
    patientEntry = PatientACManager.select_ByName('PACD.db', patientName)
    tokenID = patientEntry[0]['TokenID']
    
    #need to call SC, use tokenID to find tokenID saved in SC
    
    return jsonify({'TokenID' : tokenID}), 201
    
#POST req
@app.route('/test/api/v1.0/dt/create/patient_entry', methods=['POST'])
def create_patient_entry():
	#Token missing, deny access
	req_data = json.loads(request.data)
	if('Name' not in req_data):
		abort(401, {'message': 'Token missing, deny access'})
	
	#Authorization process
	'''if(not CapPolicy.is_valid_access_request(request)):
		abort(401, {'message': 'Authorization fail, deny access'})'''
		
	if not request.json:
		abort(400, {'message': 'No data in parameter for operation.'})
    
	data_in = [req_data['Name'], req_data['TokenID'], req_data['InstitutionName'], req_data['InstitutionAddress']]
    
    
    #call SC to add patient token
    
    #call db to add patient entry into PACD database, insert data as a list
	PatientACManager.insert_entry('PACD.db', data_in)
    
	#return jsonify({'project_data': project}), 201
	return jsonify({'result': 'Succeed'}), 201    
    
#POST req
@app.route('/test/api/v1.0/dt/create/inst_reg', methods=['POST'])
def create_institution_registry():
	#Token missing, deny access
	req_data = json.loads(request.data)
	if('Name' not in req_data):
		abort(401, {'message': 'Token missing, deny access'})
	
    #what authorization to include? this wouldn't involve SC
    
	#Authorization process
	'''if(not CapPolicy.is_valid_access_request(request)):
		abort(401, {'message': 'Authorization fail, deny access'})'''
		
	if not request.json:
		abort(400, {'message': 'No data in parameter for operation.'})

    data_in = [req_data['Name'], req_data['SC_Address']]
	
    #call to db_layer to add entry into REGD.db database
    RegistrationManager.insert_entry('REGD.db', data_in)
    
	return jsonify({'result': 'Succeed'}), 201     

#GET req
@app.route('/test/api/v1.0/dt', methods=['GET'])
def get_projects():
	#Token missing, deny access
	if(request.data=='{}'):
		abort(401, {'message': 'Token missing, deny access'})
		
	#Authorization process
	#if(not CapPolicy.is_valid_access_request(request)):
	#if(not RBACPolicy.is_valid_access_request(request)):
	#if(not ABACPolicy.is_valid_access_request(request)):
	#	abort(401, {'message': 'Authorization fail, deny access'})
	return jsonify({'result': 'Succeed', 'projects': projects}), 201
	
#GET req for specific ID
@app.route('/test/api/v1.0/dt/project', methods=['GET'])
def get_project():
	#Token missing, deny access
	if(request.data=='{}'):
		abort(401, {'message': 'Token missing, deny access'})
		
	#Authorization process
	#if(not CapPolicy.is_valid_access_request(request)):
	#if(not RBACPolicy.is_valid_access_request(request)):
	#if(not ABACPolicy.is_valid_access_request(request)):
	#	abort(401, {'message': 'Authorization fail, deny access'})
	#print request.data
	project_id = request.args.get('project_id', default = 1, type = int)
	#project_id = int(request.args['project_id'])
	
	project = [project for project in projects if project['id'] == project_id]
	if len(project) == 0:
		abort(404, {'message': 'No data found'})
	return jsonify({'result': 'Succeed', 'project': project[0]}), 201
	
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