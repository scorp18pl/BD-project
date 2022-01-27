#! /bin/bash
g++ data_gen.cpp -o data_gen
./data_gen
rm data_gen
psql -h 127.0.0.1 -U scorp2 planet_search -f planet_search.sql
psql -h 127.0.0.1 -U scorp2 planet_search -f insert_elements.sql
psql -h 127.0.0.1 -U scorp2 planet_search -f insert_rest.sql