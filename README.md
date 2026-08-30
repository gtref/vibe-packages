# vibe packages

> [!WARNING]
> This is an AI generated and maintained package repository. Use at your own risk.

Welcome to **vibe packages**, a repository for various software packages managed by AI.

## Navigation
- [Stable](./dists/stable)
- [Dev](./dists/dev)

## Security
To use these packages, you must import our GPG public key:
```bash
sudo mkdir -p /etc/apt/keyrings
curl -sS https://gtref.github.io/vibe-packages/public.key | sudo gpg --dearmor -o /etc/apt/keyrings/vibe-packages.gpg
```

## Adding the Repository
```bash
echo "deb [signed-by=/etc/apt/keyrings/vibe-packages.gpg] https://gtref.github.io/vibe-packages stable main" | sudo tee /etc/apt/sources.list.d/vibe-packages.list
sudo apt update
```

## List Packages
You can list the available packages using `curl`:
```bash
# For Stable amd64
curl -s https://gtref.github.io/vibe-packages/dists/stable/main/binary-amd64/Packages | grep Package:

# For Stable arm64
curl -s https://gtref.github.io/vibe-packages/dists/stable/main/binary-arm64/Packages | grep Package:
```

## Log
Progress and changes are tracked in the `.ai/` directory.
- Current Log: [.ai/log[5].md](.ai/log[5].md)
- Previous Logs: [.ai/log[4].md](.ai/log[4].md), [.ai/log[3].md](.ai/log[3].md), [.ai/log[2].md](.ai/log[2].md), [.Jules/log[1].md](.Jules/log[1].md)
