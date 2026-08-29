# Progress Log - log[5]

## [2026-02-12] - Add Documentation for Adding Packages & Automate GPG Public Key Export
- Added instructions to `README.md` on how to create Debian packages, build them using `scripts/manage_repo.py build`, place them in `pool/main/`, and update repository indices using `scripts/manage_repo.py update <dist>`.
- Updated `scripts/manage_repo.py` to automatically export the GPG public key to `public.key` whenever `update_repo` is run, preventing key mismatch issues.
- Added guidance to `README.md` on setting execute permissions (`chmod +x`) on package scripts/binaries before building.
- Updated `generate_index_html` in `scripts/manage_repo.py` so that `dists/stable/index.html` and `dists/dev/index.html` link parent `../` back to the repository root (`../../`).
