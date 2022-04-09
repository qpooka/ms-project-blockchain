pragma solidity >=0.4.22 <0.9.0;

//SPDX-License-Identifier: GPL-3.0

contract EHR_ACToken_Proj {

	/*
		data structure for AC token
		unique patient id (in this case, address in mapping) for identification
		access control list, made of strings maybe? or some other
			identifier for institutions
		basic patient information like name and gender
	*/
	struct AccessControlToken {
		string name;
		string gender;
		// uint256 issueDate;
		
		// keep aligned, used to easily return a string array for query
		string[] authInstitutionNames;
		address[] authInstitutions;
		
		uint8 institutionAmount;
		//mapping(address => string) authorizedInstitutions;
			
	}
	
	mapping(address => AccessControlToken) acTokens;
	address superInstitution;
	
	event OnValueChanged(address indexed _from, uint8 _value);
	
	constructor () public {
		superInstitution = msg.sender; //initialized with contract creator
	}
	
	// create/initialize token, return address created
	function createToken(string memory tokenId,
						string memory institutionName,
						string memory institutionAddr,
						string memory patientName,
						string memory patientGender) public returns (bool) {
						
		// check for institution that is making the check
		// allow contract creator and institutions on the AC list
		
		bytes32 aHash = keccak256(abi.encodePacked(tokenId));
		address newTokenIdAddress = address(uint160(uint256(aHash)));
		
		// check if token is empty
		// if not empty, don't try to "make" a new one
		
		bytes memory nameBytes = bytes(acTokens[newTokenIdAddress].name);
		bytes memory genderBytes = bytes(acTokens[newTokenIdAddress].gender);
		
		if( (acTokens[newTokenIdAddress].institutionAmount != 0) || 
			(nameBytes.length != 0) ||
			(genderBytes.length != 0) ) {
			return false;
		}
		
		if ( (msg.sender == superInstitution) ) {
			
			// acTokens[newTokenIdAddress].authorizedInstitutions[msg.sender] = institutionName;
			
			bytes32 tempInstAddr = keccak256(abi.encodePacked(institutionAddr));
			address newInstAddr = address(uint160(uint256(tempInstAddr)));
			
			acTokens[newTokenIdAddress].authInstitutionNames.push(institutionName);
			acTokens[newTokenIdAddress].authInstitutions.push(newInstAddr);
			
			acTokens[newTokenIdAddress].name = patientName;
			acTokens[newTokenIdAddress].gender = patientGender;
			// acTokens[newTokenIdAddress].issueDate = block.timestamp;
			acTokens[newTokenIdAddress].institutionAmount = 1;
			emit OnValueChanged(newTokenIdAddress, acTokens[newTokenIdAddress].institutionAmount);
			
			return true;
		}
		else {
			return false;
		}
		
	}
	
	// find/query token, return data in token
	function queryTokenData(string memory tokenId) public view returns (
																	string memory,
																	string memory,
																	uint8,
																	string memory) {
		
		string memory nameN = "";
		string memory genderN = "";
		// uint256 issueDateN = 0;
		uint8 institutionAmountN = 0;
		string memory authInstitutionNamesN = "";
		
		bytes32 aHash = keccak256(abi.encodePacked(tokenId));
		address tokenIdAddress = address(uint160(uint256(aHash)));
		
		if( (msg.sender == superInstitution) ) {
			nameN = acTokens[tokenIdAddress].name;
			genderN = acTokens[tokenIdAddress].gender;
			institutionAmountN = acTokens[tokenIdAddress].institutionAmount;
			// authInstitutionNamesN = acTokens[tokenIdAddress].authInstitutionNames;
			// concatenate elements of authInstitutionNames to a string
			for(uint8 i = 0; i < institutionAmountN; i++) {
				authInstitutionNamesN = string(abi.encodePacked(authInstitutionNamesN,
																acTokens[tokenIdAddress].authInstitutionNames[i]));
				// add split char ,
				if(i<institutionAmountN-1){
					authInstitutionNamesN = string(abi.encodePacked(authInstitutionNamesN,","));
				}
			}
		}
		return( nameN,
				genderN,
				// issueDateN,
				institutionAmountN,
				authInstitutionNamesN
				);
	}
	
	// add to AC list in token
	// input - tokenID, new institution for AC list, id of institution adding to AC list
	// newInstitutionAddr should correcpond to address of account
	function addInstitution(string memory tokenId,
						string memory newInstitutionName,
						string memory newInstitutionAddr) public returns (bool) {
		
		bytes32 aHash = keccak256(abi.encodePacked(tokenId));
		address tokenIdAddress = address(uint160(uint256(aHash)));
		
		bytes32 temp = keccak256(abi.encodePacked(newInstitutionAddr));
		address newInstitutionAddress = address(uint160(uint256(temp)));
		
		if( (msg.sender == superInstitution) ) {				
			// acTokens[tokenIdAddress].authorizedInstitutions[msg.sender] = newInstitutionName;
			
			acTokens[tokenIdAddress].authInstitutionNames.push(newInstitutionName);
			acTokens[tokenIdAddress].authInstitutions.push(newInstitutionAddress);
			
			acTokens[tokenIdAddress].institutionAmount += 1;
			emit OnValueChanged(tokenIdAddress, acTokens[tokenIdAddress].institutionAmount);
			
			return true;
		}
		else {
			return false;
		}
	}
	
	//delete institution in AC list
	function deleteInstitution(string memory tokenId,
								string memory instAddr) public returns (bool) {
		
		bytes32 aHash = keccak256(abi.encodePacked(tokenId));
		address tokenIdAddress = address(uint160(uint256(aHash)));
		
		bytes32 temp = keccak256(abi.encodePacked(instAddr));
		address instAddress = address(uint160(uint256(temp)));
		
		(bool found, uint index) = findInstitution(tokenId, instAddress);
		
		if( (msg.sender == superInstitution) && (found == true)	) {
			
			
			uint end = acTokens[tokenIdAddress].institutionAmount - 1;
			acTokens[tokenIdAddress].authInstitutionNames[index] = acTokens[tokenIdAddress].authInstitutionNames[end];
			acTokens[tokenIdAddress].authInstitutions[index] = acTokens[tokenIdAddress].authInstitutions[end];
			delete acTokens[tokenIdAddress].authInstitutionNames[end];
			delete acTokens[tokenIdAddress].authInstitutions[end];
			
			acTokens[tokenIdAddress].institutionAmount -= 1;
			emit OnValueChanged(tokenIdAddress, acTokens[tokenIdAddress].institutionAmount);
			
			return true;
		}
		else {
			return false;
		}
	}
	
	// check token for institution, return true or false
	function checkToken(string memory tokenId,
						string memory institutionAddr) public view returns (bool) {
		
		bytes32 temp = keccak256(abi.encodePacked(institutionAddr));
		address institutionAddress = address(uint160(uint256(temp)));
		
		(bool qualified,) = findInstitution(tokenId, institutionAddress);
		return qualified;
		
	}
	
	// tx.origin vs msg.sender
	
	// helper function to find institution
	function findInstitution(string memory tokenId,
							 address instAddress) private view returns (bool, uint) {
		
		bytes32 aHash = keccak256(abi.encodePacked(tokenId));
		address tokenIdAddress = address(uint160(uint256(aHash)));
		
		uint8 limit = acTokens[tokenIdAddress].institutionAmount;
		
		for(uint8 i = 0; i < limit; i++) {
			if(acTokens[tokenIdAddress].authInstitutions[i] == instAddress) {
				return (true, i);
			}
		}
		return (false, 0);
	}
	
}

// only 1 institution can add, delete, and see all token data

// bytes32 tempName = keccak256(abi.encodePacked(acTokens[tokenIdAddress].authorizedInstitutions[tx.origin]));
// below can compare strings
// tempName == keccak256(abi.encodePacked(institutionName))
