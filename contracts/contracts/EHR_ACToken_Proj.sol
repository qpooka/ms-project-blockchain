pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2; //natively supported on later solidity versions
//SPDX-License-Identifier: GPL-3.0

// issue - returning dynamic string array is not well supported on earlier solidity versions

contract EHR_ACToken_Proj {

	/*
		data structure for AC token
		unique patient id (in this case, address in mapping) for identification
		access control list, made of strings maybe? or some other
			identifier for institutions
		basic patient information like name and gender
	*/
	struct AccessControlToken {
		uint idCounter;
		
		string name;
		string gender;
		uint256 issueDate;
		
		// built-in dynamic array or mapping?
		
		// keep aligned, used to easily return a string array for query
		string[] authInstitutionNames;
		address[] authInstitutions;
		
		uint institutionAmount;
		//mapping(address => string) authorizedInstitutions;
		
		// should there be other fields in token?
	}
	
	// address is token id, that is "kinda" randomly generated
	// 		using keccak256(id, current time, address of institution)
	
	mapping(address => AccessControlToken) acTokens;
	address superInstitution;
	uint counter;
	
	event OnValueChanged(address indexed _from, uint _value);
	
	constructor () public {
		counter = 0;
		superInstitution = msg.sender; //initialized with contract creator
	}
	
	// create/initialize token, return address created
	function createToken(string memory institutionName,
						string memory patientName,
						string memory patientGender) public returns (bool, address) {
						
		// check for institution that is making the check
		// allow contract creator and institutions on the AC list
		if ( (msg.sender == superInstitution) ) {
		
			counter += 1;
			bytes32 aHash = keccak256(abi.encodePacked(counter, block.timestamp, msg.sender));
			address newTokenIdAddress = address(uint160(uint256(aHash)));
			
			acTokens[newTokenIdAddress].idCounter = counter;
			
			// acTokens[newTokenIdAddress].authorizedInstitutions[msg.sender] = institutionName;
			acTokens[newTokenIdAddress].authInstitutionNames.push(institutionName);
			acTokens[newTokenIdAddress].authInstitutions.push(msg.sender);
			
			acTokens[newTokenIdAddress].name = patientName;
			acTokens[newTokenIdAddress].gender = patientGender;
			acTokens[newTokenIdAddress].issueDate = block.timestamp;
			acTokens[newTokenIdAddress].institutionAmount = 1;
			emit OnValueChanged(newTokenIdAddress, acTokens[newTokenIdAddress].institutionAmount);
			
			return (true, newTokenIdAddress);
		}
		else
			return (false, address(0)); //return dummy address
	}
	
	// find/query token, return data in token
	function queryTokenData(address tokenIdAddress) public view returns (uint,
																	string memory,
																	string memory,
																	uint256,
																	uint,
																	string[] memory) {
		if( (msg.sender == superInstitution) ) {
			return(	acTokens[tokenIdAddress].idCounter,
					acTokens[tokenIdAddress].name,
					acTokens[tokenIdAddress].gender,
					acTokens[tokenIdAddress].issueDate,
					acTokens[tokenIdAddress].institutionAmount,
					acTokens[tokenIdAddress].authInstitutionNames
					);
		}
		else {
			uint idCounterN = 0;
			string memory nameN = "";
			string memory genderN = "";
			uint256 issueDateN = 0;
			uint institutionAmountN = 0;
			string[] memory authNamesN = new string[](1);
			
			return(idCounterN,
					nameN,
					genderN,
					issueDateN,
					institutionAmountN,
					authNamesN
					);
		}
			
	}
	
	// add to AC list in token
	// input - tokenID, new institution for AC list, id of institution adding to AC list
	function addInstitution(address tokenIdAddress,
						string memory newInstitutionName,
						address newInstitutionAddress) public returns (bool) {
		if( (msg.sender == superInstitution)	) {				
			// acTokens[tokenIdAddress].authorizedInstitutions[msg.sender] = newInstitutionName;
			
			acTokens[tokenIdAddress].authInstitutionNames.push(newInstitutionName);
			acTokens[tokenIdAddress].authInstitutions.push(newInstitutionAddress);
			
			acTokens[tokenIdAddress].institutionAmount = acTokens[tokenIdAddress].institutionAmount + 1;
			emit OnValueChanged(tokenIdAddress, acTokens[tokenIdAddress].institutionAmount);
			
			return true;
		}
		else
			return false;
	}
	
	//delete institution in AC list
	function deleteInstitution(address tokenIdAddress,
								address instAddress) public returns (bool) {
		
		if( (msg.sender == superInstitution)	) {
			(, uint index) = findInstitution(tokenIdAddress, instAddress);
			
			uint end = acTokens[tokenIdAddress].institutionAmount - 1;
			acTokens[tokenIdAddress].authInstitutionNames[index] = acTokens[tokenIdAddress].authInstitutionNames[end];
			acTokens[tokenIdAddress].authInstitutions[index] = acTokens[tokenIdAddress].authInstitutions[end];
			delete acTokens[tokenIdAddress].authInstitutionNames[end];
			delete acTokens[tokenIdAddress].authInstitutions[end];
			
			acTokens[tokenIdAddress].institutionAmount = acTokens[tokenIdAddress].institutionAmount - 1;
			emit OnValueChanged(tokenIdAddress, acTokens[tokenIdAddress].institutionAmount);
			
			return true;
		}
		else
			return false;
	}
	
	// check token for institution, return true or false
	function checkToken(address tokenIdAddress,
						address institutionAddress) public view returns (bool) {
		
		(bool qualified,) = findInstitution(tokenIdAddress, msg.sender);
		if( (msg.sender == superInstitution) || (qualified == true) ) {
			(bool find,) = findInstitution(tokenIdAddress, institutionAddress);
			return find;
		}
		else
			return false;
	}
	
	// tx.origin vs msg.sender
	
	// helper function to find institution
	function findInstitution(address tokenIdAddress,
							 address instAddress) private view returns (bool, uint) {
							 
		uint limit = acTokens[tokenIdAddress].institutionAmount;
		
		for(uint i = 0; i < limit; i++) {
			if(acTokens[tokenIdAddress].authInstitutions[i] == instAddress) 
				return (true, i);
		}
		return (false, 0);
	}
}

// only 1 institution can add, delete, and see all token data

// bytes32 tempName = keccak256(abi.encodePacked(acTokens[tokenIdAddress].authorizedInstitutions[tx.origin]));
// below can compare strings
// tempName == keccak256(abi.encodePacked(institutionName))
