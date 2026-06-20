#!/bin/bash
LOGFILE="./creation.log"

echo -n "Enter database server IP address: "
read host
echo -n "Enter PostgreSQL admin's password on $host: "
read -s admin_password
echo -e "\n"

echo "---------------------------------------" >> "$LOGFILE"
echo "-- " $(date ) " --" >> "$LOGFILE"
echo "- Database sbms on " $host " -" >> "$LOGFILE"
echo "---------------------------------------" >> "$LOGFILE"
./automation.sh $host $admin_password  >> "$LOGFILE"
echo "End of scripts."  >> "$LOGFILE"
echo -e "End of scripts."
