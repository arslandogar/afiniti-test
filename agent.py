#!/usr/bin/env python

import sys, os, signal
import optparse
import pprint
import shutil
import psycopg2
import netsnmpagent
from configparser import ConfigParser


def connectDB(filename='config/dbConfig.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(
            section, filename))

    return db


#return the latest value of the column ‘signalValue'
#from table named ‘snmpSignals’ in a database named ‘afinitiTest’
def fetchLatestSignal():
    """ Connect to the PostgreSQL database server
        Return the latest value of the column ‘signalValue' 
        from table named ‘snmpSignals’ in a database named ‘afinitiTest’  """
    getLatestSignal = None
    conn = None
    try:
        # read connection parameters
        params = connectDB()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            'SELECT "signalValue" FROM public."snmpSignals" ORDER BY "signalTime" DESC LIMIT 1'
        )

        getLatestSignal = cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return getLatestSignal[0]


# Make sure we use the local copy, not a system-wide one
sys.path.insert(0, os.path.dirname(os.getcwd()))

prgname = sys.argv[0]

# Process command line arguments
parser = optparse.OptionParser()
parser.add_option(
    "-m",
    "--mastersocket",
    dest="mastersocket",
    help=
    "Sets the transport specification for the master agent's AgentX socket",
    default="/var/run/agentx/master")
parser.add_option("-p",
                  "--persistencedir",
                  dest="persistencedir",
                  help="Sets the path to the persistence directory",
                  default="/var/lib/net-snmp")
(options, args) = parser.parse_args()

# Get terminal width for usage with pprint
rows, columns = os.popen("stty size", "r").read().split()

# First, create an instance of the netsnmpAgent class. We specify the
# fully-qualified path to AFINITI-TEST-MIB.txt ourselves here, so that you
# don't have to copy the MIB to /usr/share/snmp/mibs.
try:
    agent = netsnmpagent.netsnmpAgent(AgentName="Agent",
                                      MasterSocket=options.mastersocket,
                                      PersistenceDir=options.persistencedir,
                                      MIBFiles=["AFINITI-TEST-MIB.txt"])
except netsnmpagent.netsnmpAgentException as e:
    print("{0}: {1}".format(prgname, e))
    sys.exit(1)

# Then we create all SNMP variables we're willing to serve.
versionNumber = agent.OctetString(oidstr="AFINITI-TEST-MIB::versionNumber",
                                  initval="6.6.1")
latestSignal = agent.OctetString(oidstr="AFINITI-TEST-MIB::latestSignal",
                                 initval=fetchLatestSignal())
diskSpace = agent.Counter64(oidstr="AFINITI-TEST-MIB::diskSpace",
                            initval=shutil.disk_usage("/var/log").used)

# Finally, we tell the agent to "start". This actually connects the
# agent to the master agent.
try:
    agent.start()
except netsnmpagent.netsnmpAgentException as e:
    print("{0}: {1}".format(prgname, e))
    sys.exit(1)

print("{0}: AgentX connection to snmpd established.".format(prgname))


# Helper function that dumps the state of all registered SNMP variables
def DumpRegistered():
    for context in agent.getContexts():
        print("{0}: Registered SNMP objects in Context \"{1}\": ".format(
            prgname, context))
        vars = agent.getRegistered(context)
        pprint.pprint(vars, width=columns)
        print


DumpRegistered()


# Install a signal handler that terminates our simple agent when
# CTRL-C is pressed or a KILL signal is received
def TermHandler(signum, frame):
    global loop
    loop = False


signal.signal(signal.SIGINT, TermHandler)
signal.signal(signal.SIGTERM, TermHandler)


# Install a signal handler that dumps the state of all registered values
# when SIGHUP is received
def HupHandler(signum, frame):
    DumpRegistered()


signal.signal(signal.SIGHUP, HupHandler)

# The agent's main loop. We loop endlessly until our signal
# handler above changes the "loop" variable.
print(
    "{0}: Serving SNMP requests, send SIGHUP to dump SNMP object state, press ^C to terminate..."
    .format(prgname))
loop = True
while (loop):
    # Block and process SNMP requests, if available
    agent.check_and_process()

print("{0}: Terminating.".format(prgname))
agent.shutdown()