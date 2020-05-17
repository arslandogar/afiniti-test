# Engineering Talent Hunt Assignment

Contains an implementation of an SNMP agent that exposes three custom enterprise OIDs.

## How to Run

Install the these dependencies if not already installed.

 - Net-SNMP
 - python-netsnmpagent
 - psycopg2
 - configparser (Used to store Postgres connection parameters in a separate file)

Run "run_agent.sh" script and it will set up a custom, minimal snmpd instance that runs under your ordinary user account and separate from any system-wide running snmpd. It will even tell you the SNMP commands that you can use to test that everything works.

If instead you want to run the agent against your system-wide snmpd instance, your /etc/snmp/snmpd.conf path must be configured appropriately.

To connect to Postgres database, change connection parameters in config/dbConfig.ini file. Use the database.sql file to create tables and insert some data in a database named ‘afinitiTest’

## Testing
After running the script, run these commands in another console.

 - Get version number
	 
	 `snmpget -v 2c -c public -M+. localhost:5555 .1.3.6.1.4.1.53864.1.0`

- Get latest signal value
	
	`snmpget -v 2c -c public -M+. localhost:5555 .1.3.6.1.4.1.53864.2.0`

- Get size of /var/log folder in bytes
	
	`snmpget -v 2c -c public -M+. localhost:5555 .1.3.6.1.4.1.53864.3.0`


## Breakdown of My Tasks

- Understand SNMP protocol.
- Understand MIBs and OIDs.
- Write a custom MIB definition file.
- Learn about net-snmp and what are different ways to extend its functionality.
- Learn how to use python-netsnmpagent.
- Set up an snmp agent with custom enterprise OIDs using python-netsnmpagent module.
- Write script to setup an snmpd instance.
- Testing

## Languages Used

- Python 

  Main reason for using Python was its modules. netsnmpagent provides a very convenient way to write a sub-agent using AgentX protocol.
I initaily tried implementing sub-agent using a bash script but found it a bit complex to connect and query from database so I switched to Python because psycopg2 makes using PostgresSQL database in Python code very easy and straightforward.

- Shell 
	
	Shell scripting to set up an snmpd instance.

## A Better Approach

Currently, while running, the agent only handle requests and does not update data. To update the data we have to restart the agent. A better approach would be to handle data update process in a separate thread.
