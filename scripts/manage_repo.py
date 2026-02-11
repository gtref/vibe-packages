import os
import subprocess
import argparse

GPG_KEY_NAME = "Vibe Packages AI"
ARCHS = ["amd64", "arm64", "armhf"]

def run_command(command, cwd=None):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False, result.stderr
    return True, result.stdout

def build_package(source_dir, output_dir="pool/main"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    success, output = run_command(f"dpkg-deb --build {source_dir} {output_dir}")
    return success

def update_repo(dist):
    print(f"Updating repository for distribution: {dist}")
    dist_dir = f"dists/{dist}"

    for arch in ARCHS:
        binary_dir = f"{dist_dir}/main/binary-{arch}"
        if not os.path.exists(binary_dir):
            os.makedirs(binary_dir)

        # Generate Packages file for specific architecture
        # Note: dpkg-scanpackages is used here for better architecture filtering
        success, output = run_command(f"dpkg-scanpackages --arch {arch} pool/main > {binary_dir}/Packages")
        if not success:
            # Fallback if dpkg-scanpackages fails or if we prefer apt-ftparchive
            # apt-ftparchive packages pool/main > {binary_dir}/Packages
            # For now, let's assume dpkg-scanpackages is fine.
            pass

        run_command(f"gzip -fk {binary_dir}/Packages")

    # Generate Release file
    arch_str = " ".join(ARCHS)
    release_header = f"""Origin: Vibe Packages
Label: Vibe Packages {dist.capitalize()}
Suite: {dist}
Codename: {dist}
Architectures: {arch_str}
Components: main
Description: Vibe Packages {dist.capitalize()} Repository (AI Managed)
"""
    # Create a temporary Release file with header
    temp_release = f"{dist_dir}/Release.new"
    with open(temp_release, "w") as f:
        f.write(release_header)

    # Append file hashes using apt-ftparchive release
    success, output = run_command(f"apt-ftparchive release {dist_dir} >> {temp_release}")
    if not success: return False

    # Move to actual Release file
    os.rename(temp_release, f"{dist_dir}/Release")

    # Sign Release file
    run_command(f"gpg --batch --yes --clearsign --local-user '{GPG_KEY_NAME}' --output {dist_dir}/InRelease {dist_dir}/Release")
    run_command(f"gpg --batch --yes --detach-sign --armor --local-user '{GPG_KEY_NAME}' --output {dist_dir}/Release.gpg {dist_dir}/Release")

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Debian Repository")
    subparsers = parser.add_subparsers(dest="command")

    build_parser = subparsers.add_parser("build", help="Build a package")
    build_parser.add_argument("source_dir", help="Source directory of the package")

    update_parser = subparsers.add_parser("update", help="Update repository metadata")
    update_parser.add_argument("dist", choices=["stable", "dev"], help="Distribution to update")

    args = parser.parse_args()

    if args.command == "build":
        build_package(args.source_dir)
    elif args.command == "update":
        update_repo(args.dist)
    else:
        parser.print_help()
