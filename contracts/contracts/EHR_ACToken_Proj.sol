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
		string name;
		string gender;
		uint256 issueDate;
		
		// keep aligned, used to easily return a string array for query
		string[] authInstitutionNames;
		address[] authInstitutions;
		
		uint institutionAmount;
		//mapping(address => string) authorizedInstitutions;
			
	}
	
	mapping(address => AccessControlToken) acTokens;
	address superInstitution;
	
	event OnValueChanged(address indexed _from, uint _value);
	
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
		
		
		if ( (msg.sender == superInstitution) ) {
			bytes32 aHash = keccak256(abi.encodePacked(tokenId));
			address newTokenIdAddress = address(uint160(uint256(aHash)));
			
			// acTokens[newTokenIdAddress].authorizedInstitutions[msg.sender] = institutionName;
			
			bytes32 tempInstAddr = keccak256(abi.encodePacked(institutionAddr));
			address newInstAddr = address(uint160(uint256(tempInstAddr)));
			
			acTokens[newTokenIdAddress].authInstitutionNames.push(institutionName);
			acTokens[newTokenIdAddress].authInstitutions.push(newInstAddr);
			
			acTokens[newTokenIdAddress].name = patientName;
			acTokens[newTokenIdAddress].gender = patientGender;
			acTokens[newTokenIdAddress].issueDate = block.timestamp;
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
																	uint256,
																	uint,
																	string[] memory) {
		
		string memory nameN = "";
		string memory genderN = "";
		uint256 issueDateN = 0;
		uint institutionAmountN = 0;
		string[] memory authNamesN = new string[](1);
		
		bytes32 aHash = keccak256(abi.encodePacked(tokenId));
		address tokenIdAddress = address(uint160(uint256(aHash)));
		
		if( (msg.sender == superInstitution) ) {
			return( acTokens[tokenIdAddress].name,
					acTokens[tokenIdAddress].gender,
					acTokens[tokenIdAddress].issueDate,
					acTokens[tokenIdAddress].institutionAmount,
					acTokens[tokenIdAddress].authInstitutionNames
					);
		}
		else {
			return( nameN,
					genderN,
					issueDateN,
					institutionAmountN,
					authNamesN
					);
		}
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
			
			acTokens[tokenIdAddress].institutionAmount = acTokens[tokenIdAddress].institutionAmount + 1;
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
		
		if( (msg.sender == superInstitution)	) {
			(, uint index) = findInstitution(tokenId, instAddress);
			
			uint end = acTokens[tokenIdAddress].institutionAmount - 1;
			acTokens[tokenIdAddress].authInstitutionNames[index] = acTokens[tokenIdAddress].authInstitutionNames[end];
			acTokens[tokenIdAddress].authInstitutions[index] = acTokens[tokenIdAddress].authInstitutions[end];
			delete acTokens[tokenIdAddress].authInstitutionNames[end];
			delete acTokens[tokenIdAddress].authInstitutions[end];
			
			acTokens[tokenIdAddress].institutionAmount = acTokens[tokenIdAddress].institutionAmount - 1;
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
		if( (msg.sender == superInstitution) || (qualified == true) ) {
			return qualified;
		}
		else {
			return false;
		}
	}
	
	// tx.origin vs msg.sender
	
	// helper function to find institution
	function findInstitution(string memory tokenId,
							 address instAddress) private view returns (bool, uint) {
		
		bytes32 aHash = keccak256(abi.encodePacked(tokenId));
		address tokenIdAddress = address(uint160(uint256(aHash)));
		
		uint limit = acTokens[tokenIdAddress].institutionAmount;
		
		for(uint i = 0; i < limit; i++) {
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
