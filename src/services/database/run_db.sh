#!/bin/bash
docker run --name db-instance -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

# Connect to db: psql -h localhost -p 5432 -U postgres
# dummy password: mysecretpassword
