======No. 1 ======
Name: Integer Overflow and Underflow 
ID: 101 
Description: This binary add operation can result in integer overflow. 
Location: 114 
Code: send it back. throw; } /* Public variables of the token */ /* NOTE: The following variables are OPTIONAL vanities. One does not have to include them. They allow one to customise the token contract & in no way influences the core functionality. Some wallets/interfaces might not even bother to look at this information. */ string public name;                   //fancy name: eg Simon Bucks uint8 public decimals;                //How many decimals to show. ie. There could 1000 base units with 3 decimals. Meaning 0.980 SBX = 980 base units. It's like comparing 1 wei to 1 ether. string public symbol;                 //An identifier: eg SBX string public version = 'H0.1';       //human 0.1 standard. Just an arbitrary versioning scheme. function HumanStandardToken( uint256 _initialAmount, string _tokenName, uint8 _decimalUnits, string _tokenSymbol ) { balances[msg.sender] = _initialAmount;               // Give the creator all initial tokens totalSupply = _initialAmount;                        // Update total supply name = _tokenName;                                   // Set the name for display purposes decimals = _decimalUnits;                            // Amount of decimals for display purposes symbol = _tokenSymbol;                               // Set the symbol for display purposes } /* Approves and then calls the receiving contract */ function approveAndCall(address _spender, uint256 _value, bytes _extraData) returns (bool success) { allowed[msg.sender][_spender] = _value; Approval(msg.sender, _spender, _value); //call the receiveApproval function on the contract you want to be notified. This crafts the function signature manually so one doesn't have to include a contract in here just for this. //receiveApproval(address _from, uint256 _value, address _tokenContract, bytes _extraData) //it is assumed that when does this that the call *should* succeed, otherwise one would use vanilla approve instead. if(!_spender.call(bytes4(bytes32(sha3("receiveApproval(address,uint256,address,bytes)"))), msg.sender, _value, this, _extraData)) { throw; } return true; } } 
Reference[1]: https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-101 
Reference[2]:  

======No. 2 ======
Name: Unchecked Call Return Value 
ID: 104 
Description:   
Location:  146-155 
Code:  
Reference[1]: https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-104 
Reference[2]: https://github.com/trailofbits/slither/wiki/Vulnerabilities-Description#low-level-calls[0m 

======No. 3 ======
Name: Conformance To Solidity Naming Conventions 
ID: 016 
Description:   is not in mixedCase 
Location:  80-82 
Code:  
Reference[1]:  
Reference[2]: https://github.com/trailofbits/slither/wiki/Vulnerabilities-Description#conformance-to-solidity-naming-conventions[0m 

======No. 4 ======
Name: State Variables That Could Be Declared Constant 
ID: 018 
Description:   
Location:  131-132 
Code:  
Reference[1]:  
Reference[2]: https://github.com/trailofbits/slither/wiki/Vulnerabilities-Description#state-variables-that-could-be-declared-constant[0m 

======No. 5 ======
Name: Public Function That Could Be Declared As External 
ID: 019 
Description:   should be declared external 
Location:  8-10 
Code:  
Reference[1]:  
Reference[2]: https://github.com/trailofbits/slither/wiki/Vulnerabilities-Description#public-function-that-could-be-declared-as-external[0m 

