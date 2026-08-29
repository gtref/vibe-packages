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

## Contributing / Adding Packages
To add a new Debian package (`.deb`) to the repository:

1. **Prepare the Package Directory Structure**:
   Create a package root directory containing the required files and the `DEBIAN/control` manifest:
   ```
   my-package/
   ├── DEBIAN/
   │   └── control
   └── usr/
       └── bin/
           └── my-script
   ```
   Example `DEBIAN/control` content:
   ```control
   Package: my-package
   Version: 1.0.0
   Architecture: all
   Maintainer: Your Name <you@example.com>
   Description: Brief description of my-package
   ```

2. **Build the `.deb` Package**:
   Run the repository build helper to compile the Debian package into `pool/main/`:
   ```bash
   python3 scripts/manage_repo.py build my-package
   ```
   *Note: Alternatively, if you already have a pre-built `.deb` package, copy it directly into `pool/main/`.*

3. **Update Repository Metadata**:
   Update the distribution indices and signed release metadata for the target distribution (`stable` or `dev`):
   ```bash
   python3 scripts/manage_repo.py update stable
   python3 scripts/manage_repo.py update dev
   ```

4. **Commit & Push**:
   Commit the new package in `pool/main/`, updated metadata under `dists/`, and push to the default branch to publish via GitHub Pages.

## Log
Progress and changes are tracked in the `.ai/` directory.
- Current Log: [.ai/log[5].md](.ai/log[5].md)
- Previous Logs: [.ai/log[4].md](.ai/log[4].md), [.ai/log[3].md](.ai/log[3].md), [.ai/log[2].md](.ai/log[2].md), [.Jules/log[1].md](.Jules/log[1].md)
