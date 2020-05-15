#!/bin/sh -f

PLACE=".1.3.6.1.4.1.53864"  # NET-SNMP-PASS-MIB::netSnmpPassExamples
REQ="$2"                         # Requested OID

#
#  Process SET requests by simply logging the assigned value
#      Note that such "assignments" are not persistent,
#      nor is the syntax or requested value validated
#  
if [ "$1" = "-s" ]; then
  echo $* >> /tmp/passtest.log
  exit 0
fi

#
#  GETNEXT requests - determine next valid instance
#
if [ "$1" = "-n" ]; then
  case "$REQ" in
    $PLACE|		\
    $PLACE.1.1)       RET=$PLACE.1.1 ;; 	# netSnmpPassString.0
    $PLACE.2.1)       RET=$PLACE.2.1 ;; 	# netSnmpPassInteger.1
    $PLACE.3.1)       RET=$PLACE.3.1 ;;     	# netSnmpPassTimeTicks.0
    *)         	    exit 0 ;;
  esac
else
#
#  GET requests - check for valid instance
#
  case "$REQ" in
    $PLACE.1.1|	\
    $PLACE.2.1|	\
    $PLACE.3.1)     RET=$REQ ;;
    *)         	    exit 0 ;;
  esac
fi

#
#  "Process" GET* requests - return hard-coded value
#
echo "$RET"
case "$RET" in
  $PLACE.1.1) echo "string";	node -v;				exit 0 ;;
  $PLACE.2.1) echo "string";	PGPASSWORD=chel@1905  psql -U postgres -h localhost -d afinitiTest -c "select \"signalValue"\ from public.\"snmpSignals"\"";				exit 0 ;;
  $PLACE.3.1) echo "string";	df -k /var/log;	exit 0 ;;
  *)	      echo "string";	echo "ack... $RET $REQ";	exit 0 ;;  # Should not happen
esac
