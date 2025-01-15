# OGUOGU.me: Support your tiny Challenges

## Introduction

매일매일 작은 도전을 해낼 수 있도록, 오구오구


## Development


1. deploy database & Anvil server

```bash
docker compose -f docker-compose.yaml up
```

2. Deploy Contract

```bash
cd contracts/
forge script --broadcast --rpc-url http://localhost:8545 -vvvv script/local/deploy.s.sol
```

3. Mint TestToken

```bash
cd contracts/
forge script --broadcast --rpc-url http://localhost:8545 -vvvv script/local/mint.s.sol
```

4. Deploy Server
   
```bash
cd server/
poetry run fastapi run main.py