#!/usr/bin/env python3.5

'''
========================
db_layer.py
========================
@TaskDescription: This module provide database layer API.
'''

#database should have :
#   table for dummy EHR data? or is that pre-filled somewhere else?
#   table for EHR AC list, tokenID assigned to each patient
#   what other table should be here?

import sqlite3
#from utilities import DatetimeUtil, TypesUtil, FileUtil

# returning an object that can also access columns by name
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Question: why is role and user is different tables? 

'''
PatientACManager class for manage database by using SQLite lib
'''
#include: patient name, tokenID, institution names, institution addresses
#when making token and adding institution to SC, have to store institution address and tokenID
class PatientACManager(object):
    
    #create table in db file
    #can only intialize once?
    @staticmethod
    def create_table(db_path):
        conn = sqlite3.connect(db_path) #connect instance of sqlite3 object to use methods on stored table

        #check if table already exists by counting rows
        #a row corresponds to a patient and their info
        cursor = conn.execute("SELECT name from sqlite_master where Type='table' and name='PatientACdata';")
        row_count = 0
        for row in cursor:
            row_count += 1
        
        if row_count == 0:
            #create table
            conn.execute("CREATE TABLE PatientACdata \
                        (Name                      TEXT PRIMARY KEY, \
                         Gender                    TEXT NULL,        \
                         TokenID                   TEXT NULL,        \
                         InstitutionName           TEXT NULL,        \
                         InstitutionAddress        TEXT NULL);")
        else:
            print("Table:PatientACdata already exists.")
     
     
    #Select all record from table
    #eturns instName and instAddress as string,string,string,...
    @staticmethod       
    def select_Allentry(path_db):
        conn = sqlite3.connect(path_db) 
        conn.row_factory = dict_factory
        cursor = conn.execute("SELECT Name, Gender, TokenID, InstitutionName, InstitutionAddress from PatientACdata;")

        ls_result=[]
        for row in cursor:  
            ls_result.append(row)

        conn.close()
        
        return ls_result

    #Select record from table based on Name
    #returns a list
    @staticmethod       
    def select_ByName(path_db, patient_name):
        conn = sqlite3.connect(path_db)
        
        
        conn.row_factory = dict_factory
        cursor = conn.execute("SELECT Name, Gender, TokenID, InstitutionName, InstitutionAddress from PatientACdata where Name='%s';" %(patient_name))
        
        ls_result=[]        
        for row in cursor:
            ls_result.append(row)
            
        conn.close()
        
        return ls_result
    
    #Update specific part of patient entry
    #input arg_list: Name, InstitutionName, InstitutionAddress
    def update_addInstitution(path_db, arg_list):
        conn = sqlite3.connect(path_db)
        
        user_entry = PatientACManager.select_ByName(path_db, arg_list[0])
        
        if len(user_entry) > 0:
            instNames = user_entry[0]["InstitutionName"] + "," + arg_list[1]
            instAddresses = user_entry[0]["InstitutionAddress"] + "," + arg_list[2]
            
            conn.execute("UPDATE PatientACdata set InstitutionName='%s', InstitutionAddress='%s' where Name='%s';" \
                    %(instNames, instAddresses, user_entry[0]["Name"]))
        
            conn.commit()
            
        else:
            print("could not find patient entry")
        
        conn.close()
    
    #input arg_list: Name, InstitutionName, InstitutionAddress
    def update_deleteInstitution(path_db, arg_list):
        conn = sqlite3.connect(path_db)
        
        user_entry = PatientACManager.select_ByName(path_db, arg_list[0])
        
        instNames = user_entry[0]["InstitutionName"].split(",")
        instAddresses = user_entry[0]["InstitutionAddress"].split(",")
        
        if len(user_entry) > 0:
            
            if (arg_list[1] in instNames) and (arg_list[2] in instAddresses):
                instNames.remove(arg_list[1])
                instAddresses.remove(arg_list[2])
                
                #print(instNames)
                #print(instAddresses)
                
                instNameStr = ",".join(instNames)
                instAddrStr = ",".join(instAddresses)
                
                conn.execute("UPDATE PatientACdata set InstitutionName='%s', InstitutionAddress='%s' where Name='%s';" \
                        %(instNameStr, instAddrStr, user_entry[0]["Name"]))
        
                conn.commit()
            
            else:
                print("could not find institution name or address")
            
        else:
            print("could not find patient entry")
        
        conn.close()
    
    #Update record of PatientACdata based on name
    @staticmethod   
    def update_entry(path_db, arg_list):
        conn = sqlite3.connect(path_db)
        
        conn.execute("UPDATE PatientACdata set Name='%s', Gender='%s', TokenID='%s', InstitutionName='%s', InstitutionAddress='%s' where Name='%s';" \
                    %(arg_list[1], arg_list[2], arg_list[3], arg_list[4], arg_list[5], arg_list[0]))
        
        conn.commit()
        conn.close() 

    #Insert patient entry into PatientACdata
    #institutionName and institutionAddress should be entered "one" at a time
    @staticmethod   
    def insert_entry(path_db, arg_list):    
        conn = sqlite3.connect(path_db)

        #check if user name already exist
        user_entry = PatientACManager.select_ByName(path_db, arg_list[0])
        if len(user_entry) > 0:
            print("%s already exists!" %(arg_list[0]))
        else:             
            conn.execute("INSERT INTO PatientACdata (Name, Gender, TokenID, InstitutionName, InstitutionAddress) VALUES ('%s','%s','%s','%s','%s');" \
                %(arg_list[0], arg_list[1], arg_list[2], arg_list[3], arg_list[4]));

            conn.commit()
        conn.close()
    
    #Remove table
    #for restarting local db
    def remove_table(db_path):
        conn = sqlite3.connect(db_path)
        #remove selected table
        cursor = conn.execute("DROP TABLE PatientACdata;")

    #Delete user from PatientACdata based on Name
    @staticmethod       
    def delete_ByName(path_db, user_name):
        conn = sqlite3.connect(path_db)

        conn.execute("DELETE from PatientACdata where Name = '%s';" %(user_name))
        conn.commit()
        
        conn.close()

#used for immediate identification of registered ____ (users) for institution
#is this for patients or for other institutions?
#if going the institution registry route, can have AC Policy check:
# first if institution requester is in registry db,
# then if institution is in requested patient AC token in the SC
# each can give a different fail message if either fails
# must pass both to get data
class RegistrationManager(object):
    
    #create table in db file
    @staticmethod
    def create_table(db_path):
        conn = sqlite3.connect(db_path) #connect instance of sqlite3 object to use methods on stored table

        #check if table already exists by counting rows
        #a row corresponds to a patient
        cursor = conn.execute("SELECT name from sqlite_master where Type='table' and name='RegistryData';")
        row_count = 0
        for row in cursor:
            row_count += 1
        
        if row_count == 0:
            #create table
            conn.execute("CREATE TABLE RegistryData \
                        (Name                      TEXT PRIMARY KEY, \
                         SC_Address                  TEXT NULL,        \
                                                TEXT NULL,        \
                                                TEXT NULL,        \
                                         TEXT NULL,        \
                                          TEXT NULL,        \
                                            TEXT NULL);")
        else:
            print("Table: Registry data already exists.")
    

# for institutions' dummy EHR data
# a local db, so only the instiution in charge of these EHRs has access to local
#data in it anyway
class EHR_Manager(object):

    #create table in db file
    #can only intialize once?
    @staticmethod
    def create_table(db_path):
        conn = sqlite3.connect(db_path) #connect instance of sqlite3 object to use methods on stored table

        #check if table already exists by counting rows
        #a row corresponds to a patient and their EHR
        cursor = conn.execute("SELECT name from sqlite_master where Type='table' and name='EHRdata';")
        row_count = 0
        for row in cursor:
            row_count += 1
        
        if row_count == 0:
            #create table
            conn.execute("CREATE TABLE EHRdata \
                        (Name                      TEXT PRIMARY KEY, \
                         Gender                    TEXT NULL,        \
                         Age                       TEXT NULL,        \
                         SSN                       TEXT NULL,        \
                         Medication                TEXT NULL,        \
                         Allergies                 TEXT NULL,        \
                         Address                   TEXT NULL);")
        else:
            print("Table: EHR data already exists.")
    
    #Select record from table based on Name
    #returns a list
    @staticmethod       
    def select_ByName(path_db, patient_name):
        conn = sqlite3.connect(path_db)
        
        conn.row_factory = dict_factory
        cursor = conn.execute("SELECT * from EHRdata where Name='%s';" %(patient_name))
        
        ls_result=[]        
        for row in cursor:
            ls_result.append(row)
            
        conn.close()
        
        return ls_result
        
    #Select record from table based on SSN
    #returns a list
    @staticmethod       
    def select_BySSN(path_db, patient_SSN):
        conn = sqlite3.connect(path_db)
        
        
        conn.row_factory = dict_factory
        cursor = conn.execute("SELECT * from EHRdata where SSN='%s';" %(patient_SSN))
        
        ls_result=[]        
        for row in cursor:
            ls_result.append(row)
            
        conn.close()
        
        return ls_result
     
    #Select all record from table
    #eturns medication and allergies as string,string,string,...
    @staticmethod       
    def select_Allentry(path_db):
        conn = sqlite3.connect(path_db) 
        conn.row_factory = dict_factory
        cursor = conn.execute("SELECT * from EHRdata;")

        ls_result=[]
        for row in cursor:  
            ls_result.append(row)

        conn.close()
        
        return ls_result
        
    #Insert EHR entry into EHRdata
    @staticmethod   
    def insert_entry(path_db, arg_list):    
        conn = sqlite3.connect(path_db)

        #check if user name already exist
        EHR_entry = EHR_Manager.select_ByName(path_db, arg_list[0])
        if len(EHR_entry) > 0:
            print("%s already exists!" %(arg_list[0]))
        else:             
            conn.execute("INSERT INTO EHRdata (Name, Gender, Age, SSN, Medication, Allergies, Address) \
                            VALUES ('%s','%s','%s','%s','%s','%s','%s');" \
                %(arg_list[0], arg_list[1], arg_list[2], arg_list[3], arg_list[4], arg_list[5], arg_lis[6]));

            conn.commit()
        conn.close()
    
    #Update record of EHRdata based on name
    @staticmethod   
    def update_entry(path_db, arg_list):
        conn = sqlite3.connect(path_db)
        
        conn.execute("UPDATE EHRdata set Name='%s', Gender='%s', Age='%s', SSN='%s', Medication='%s', Allergies='%s', Address='%s' where Name='%s';" \
                    %(arg_list[1], arg_list[2], arg_list[3], arg_list[4], arg_list[5], arg_list[6], arg_list[7], arg_list[0]))
        
        conn.commit()
        conn.close() 
    
    #Remove table
    #for restarting local db
    def remove_table(db_path):
        conn = sqlite3.connect(db_path)
        #remove selected table
        cursor = conn.execute("DROP TABLE EHRdata;")

    #Delete user from EHRdata based on Name
    @staticmethod       
    def delete_ByName(path_db, patient_name):
        conn = sqlite3.connect(path_db)

        conn.execute("DELETE from EHRdata where Name = '%s';" %(patient_name))
        conn.commit()
        
        conn.close()
       
def test_patient():
    #test Api
    path_db='PACD.db'
    
    # new patient AC table 
    PatientACManager.create_table(path_db)
    #PatientACManager.remove_table(path_db)

    # test insert user data
    patient_arg1 = ['Jeff', 'male', '0xb7d094a545a59610a9ef9f36afb4d640d3140cd1', 'EHR_AC_1', '0x548bdfcaeb2758ee2a8ca71d8f5baafacf5ea49f']
    patient_arg2 = ['Alice', 'female', '0x17d094a545a59610a9ef9f36afb4d640d3140cd2', 'EHR_AC_1', '0x548bdfcaeb2758ee2a8ca71d8f5baafacf5ea49f']
    PatientACManager.insert_entry(path_db, patient_arg1)
    PatientACManager.insert_entry(path_db, patient_arg2)

    #search test
    print("------search tests after inserting new patient entries-------")
    patients_list = PatientACManager.select_Allentry(path_db)
    print(patients_list)
    patients_entry = PatientACManager.select_ByName(path_db,'Jeff')
    print(patients_entry)
    print()
    
    #update - add institution test
    print("------update - add institution tests for Jeff-------")
    inst2 = ["newInst", "0xa7d094a545a59610a9ef9f36afb4d640d3140cd6"]
    inst3 = ["differentInst", "0x6e8df907de0c1bb5a6d32a21ff0042fbef0c05d0"]
    
    PatientACManager.update_addInstitution(path_db, [patient_arg1[0], inst2[0], inst2[1]])
    PatientACManager.update_addInstitution(path_db, [patient_arg1[0], inst3[0], inst3[1]])
    print(PatientACManager.select_ByName(path_db, patient_arg1[0]))
    print()

    #update - delete institution test
    print("------update - delete newInst institution tests for Jeff-------")
    PatientACManager.update_deleteInstitution(path_db, [patient_arg1[0], inst2[0], inst2[1]])
    print(PatientACManager.select_ByName(path_db, patient_arg1[0]))
    print()
    
    #delete test
    print("-------delete Jeff entry-------")
    PatientACManager.delete_ByName(path_db,patient_arg1[0])
    print(PatientACManager.select_ByName(path_db, patient_arg1[0]))
    print()

    # print eveything again
    print("-------print all entries for the last time-------")
    patients_list = PatientACManager.select_Allentry(path_db)
    print(patients_list)

def test_EHR():
    #test Api
    path_db='EHRD.db'
    
    # new EHRdata table 
    EHR_Manager.create_table(path_db)
    #EHR_Manager.remove_table(path_db)

    # test insert EHR data
    EHR_arg1 = ['Jeff', 'male', '23', '123-45-6789', 'medication1,medication2', 'shrimp', 'random address']
    EHR_arg2 = ['Alice', 'female', '24', '234-56-7891', 'random', 'milk', 'parts unknown']
    EHR_Manager.insert_entry(path_db, EHR_arg1)
    EHR_Manager.insert_entry(path_db, EHR_arg2)
    
    #search test
    print("------search tests after inserting new EHR entries-------")
    EHR_list = EHR_Manager.select_Allentry(path_db)
    print(EHR_list)
    EHR_name_entry = EHR_Manager.select_ByName(path_db,'Jeff')
    print(EHR_name_entry) #should print Jeff EHR
    EHR_SSN_entry = EHR_Manager.select_BySSN(path_db,'234-56-7891')
    print(EHR_SSN_entry) #should print Alice EHR
    print()

if __name__ == '__main__': 
    #test_patient()
    test_EHR()
    pass