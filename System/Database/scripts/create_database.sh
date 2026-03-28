psql -h $1 -U admin -W -d postgres -f structure.sql
psql -h $1 -U admin -W -d sbms -f data.sql
