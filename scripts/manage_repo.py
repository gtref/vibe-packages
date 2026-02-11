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

def generate_index(path):
    print(f"Generating index.html for {path}")
    items = sorted(os.listdir(path))
    html_content = f"<html><head><title>Index of {path}</title></head><body><h1>Index of {path}</h1><ul>"
    html_content += '<li><a href="../">Parent Directory</a></li>'
    for item in items:
        if item == "index.html": continue
        suffix = "/" if os.path.isdir(os.path.join(path, item)) else ""
        html_content += f'<li><a href="{item}{suffix}">{item}{suffix}</a></li>'
    html_content += "</ul></body></html>"
    with open(os.path.join(path, "index.html"), "w") as f:
        f.write(html_content)

def build_package(source_dir, output_dir="pool/main"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        generate_index(output_dir)
    success, output = run_command(f"dpkg-deb --build {source_dir} {output_dir}")
    return success

def update_repo(dist):
    print(f"Updating repository for distribution: {dist}")
    dist_dir = f"dists/{dist}"

    main_dir = f"{dist_dir}/main"
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
    generate_index(main_dir)

    for arch in ARCHS:
        binary_dir = f"{main_dir}/binary-{arch}"
        if not os.path.exists(binary_dir):
            os.makedirs(binary_dir)

        # Generate Packages file for specific architecture
        success, output = run_command(f"dpkg-scanpackages --arch {arch} pool/main > {binary_dir}/Packages")
        run_command(f"gzip -fk {binary_dir}/Packages")
        generate_index(binary_dir)

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

    generate_index(dist_dir)

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
