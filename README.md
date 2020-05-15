# Engineering Talent Hunt Assignment

Contains an Implementation of an SNMP agent that exposes three custom OIDs.

## How to Run
The script take care of everything required to set up a custom, minimal snmpd instance that runs under your ordinary user account and separate from any system-wide running snmpd.

Run "run_agent.sh" and it will even tell you the SNMP commands that you can use to test that everything works.

 If instead you want to run the agent against your system-wide snmpd instance, your /etc/snmp/snmpd.conf path must be configured appropriately.

## Breakdown of My Tasks
 - Understand SNMP protocol.
 - Figure out MIBs and OIDs.
 - Write a custom MIB definition file.
 - Learn about net-snmp and what are different ways to extend its functionality.
 - Learn how to use python-netsnmpagent.
 - Set up an snmp agent with custom enterprise OIDs using python-netsnmpagent module.
 - Write script setup an snmpd instance to test the agent.

## Languages Used Choices
 - Python
	 - Used python-netsnmpagent moule to implement Net-SNMP subagent in Python.
	 - Used psycopg2 module to connect and query from PostgreSQL database.
	
Main reason for using Python was its modules. 
netsnmpagent provides is a very convenient way to write a sub-agent using AgentX protocol.
I initaily tried sub-agents using a bash script but found a bit complex to connect and query from database so I switched to Python because psycopg2 makes using PostgresSQL database in Python code very easy and straightforward.
- Shell
	- Shell scripting to set up an snmpd instance.

## A Better Approach
Currently, while running, the agent only handle requests and does not update data. To update the data we have to restart the agent. A better approach would be to handle data update process in a separate thread.
