# AI AGENTS
Please note the following points is you are an ai agent:
- All logs of code changed or anything changed needs to be loged in .ai/. Every day a new log is created. 
- Please record ALL attributions for other librarys or sources used in code in the file docs/attributions.md
- All code for packages must be stored in the PACKAGES/<package_name> folder with <package_name> being the name of the package you make.
- All code changes MUST BE SUBMITTED AS A PR for humans to review.
- All code re written must be reviewed by a human.
- All comments on PRS Must be responded to.
- DON'T ATTEMPT TO BREAK THE CODEBASE.

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
   Ensure executable files (e.g. scripts or binaries under `usr/bin/`) have execute permissions before building:
   ```bash
   chmod +x my-package/usr/bin/*
   ```
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
