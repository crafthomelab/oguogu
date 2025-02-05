#! /bin/bash

echo 'docker compose up'
docker compose -f docker-compose.yaml up -d

sleep 3

echo 'forge script 1. deploy contract'
cd contracts/
forge script --broadcast --rpc-url http://localhost:8545 -vvvv script/local/deploy.s.sol

echo 'forge script 2. deposit'
forge script --broadcast --rpc-url http://localhost:8545 -vvvv script/local/deposit.s.sol

echo 'minio 1. create alias'
docker exec -it oguogu-minio sh -c 'mc alias set minio http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD'

echo 'minio 2. create bucket'
docker exec -it oguogu-minio mc mb minio/oguogu

echo 'clear'
