# Progress Log - log[5]

## [2026-02-12] - Add Documentation for Adding Packages & Automate GPG Public Key Export
- Added instructions to `README.md` on how to create Debian packages, build them using `scripts/manage_repo.py build`, place them in `pool/main/`, and update repository indices using `scripts/manage_repo.py update <dist>`.
- Updated `scripts/manage_repo.py` to automatically export the GPG public key to `public.key` whenever `update_repo` is run, preventing key mismatch issues.
