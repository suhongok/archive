# Pi Node setup on Ubuntu 24.04 (summary)

## Environment
- OS: Ubuntu 24.04
- Docker: installed
- Docker Compose v2: installed (`docker-compose-v2`)
- Pi Node CLI: installed (`pi-node` 0.2.2)
- 우리집 리눅스 컴퓨터이며 pi는 192.168.0.103 / suhong / pw:***12313t이다.

## What was done
- Verified Docker Engine and installed Docker Compose v2.
- Confirmed Pi Node CLI package already installed.
- Added current user to `docker` group (requires logout/login to apply).
- Initialized Pi Node configuration in `/home/suhong/pi-node`.
- Pulled Pi Node Docker images and started the `mainnet` container.
- Verified node status via `pi-node status`.

## Key paths
- Pi Node root: `/home/suhong/pi-node`
- Compose file: `/home/suhong/pi-node/docker-compose.yml`
- Env file: `/home/suhong/pi-node/.env`

## Current status (last check)
- Container: `mainnet` running
- Protocol state: `Joining SCP`
- Horizon: running

## Commands used (representative)
```bash
docker --version
docker compose version

pi-node --version
pi-node status

# Pull and start containers
sudo -u "$USER" -g docker docker compose -f /home/suhong/pi-node/docker-compose.yml pull
sudo -u "$USER" -g docker docker compose -f /home/suhong/pi-node/docker-compose.yml up -d

# Check node status
sudo -u "$USER" -g docker pi-node status
```

## Notes
- The Linux Pi Node is CLI-based. There is no desktop login UI.
- Node linkage with the mobile app uses **NODE_SEED / NODE_PRIVATE_KEY** from the node config. Do **not** share these values.
- You mentioned the wallet private key should match `NODE_PRIVATE_KEY` for linking; treat it as highly sensitive. 그리고 여기에 파이앱의 지갑에서 지갑의 private키를 입력하면 된다.

## Useful follow-ups
```bash
# Enable auto-update (optional)
pi-node enable-auto-update

# Logs
pi-node logs

# Stop / start
pi-node stop
pi-node start
```
