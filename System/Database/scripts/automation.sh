#!/usr/bin/expect

lassign $argv host admin_password
set timeout 120

spawn ./create_database.sh $host


expect {
    "Password:" { send "$admin_password\r" ; exp_continue }
    expect eof
}

