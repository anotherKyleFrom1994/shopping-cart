#!/bin/bash
docker build -t base-runtime -f ./docker/base/Dockerfile .
docker-compose up --build
