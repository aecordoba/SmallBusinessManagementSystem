#!/bin/bash

echo -n "Enter database server IP address: "
read host
echo -n "Enter PostgreSQL admin's password on $host: "
read -s admin_password
echo -e "\n"

echo "---------------------------------------" >> /home/adrian/Development/Applications/SmallBusinessManagementSystem/System/Database/scripts/creation.log
echo "-- " $(date ) " --" >> /home/adrian/Development/Applications/SmallBusinessManagementSystem/System/Database/scripts/creation.log
echo "- Database liniers_sur on " $host " -" >> /home/adrian/Development/Applications/SmallBusinessManagementSystem/System/Database/scripts/creation.log
echo "---------------------------------------" >> /home/adrian/Development/Applications/SmallBusinessManagementSystem/System/Database/scripts/creation.log
./automation.sh $host $admin_password  >> /home/adrian/Development/Applications/SmallBusinessManagementSystem/System/Database/scripts/creation.log
echo -e "End of scripts."
