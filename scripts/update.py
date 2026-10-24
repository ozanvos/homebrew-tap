#!/usr/bin/env python3
"""Advance the cask only to a complete, attested stable upstream release."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request

REPOSITORY = "ozanvos/monoprint"
BASE = f"https://github.com/{REPOSITORY}/releases"
CASK = Path(__file__).resolve().parents[1] / "Casks/monoprint.rb"


def read(url):
    request = urllib.request.Request(url, headers={"User-Agent": "monoprint-homebrew"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    release = json.loads(read(f"https://api.github.com/repos/{REPOSITORY}/releases/latest"))
    tag = release["tag_name"]
    require(re.fullmatch(r"v\d+\.\d+\.\d+", tag), "Expected stable version tag")
    require(not release["draft"] and not release["prerelease"], "Release must be public and stable")
    require(release["html_url"] == f"{BASE}/tag/{tag}", "Unexpected release URL")
    version = tag[1:]
    assets = {a["name"]: a for a in release["assets"]}

    def asset(name):
        entry = assets[name]
        url = f"{BASE}/download/{tag}/{name}"
        require(entry["state"] == "uploaded" and entry["browser_download_url"] == url,
                f"Unexpected asset: {name}")
        data = read(url)
        require(len(data) == entry["size"], f"Wrong size: {name}")
        require(entry["digest"] == "sha256:" + hashlib.sha256(data).hexdigest(),
                f"Wrong digest: {name}")
        return data

    manifest_bytes = asset("release.json")
    manifest = json.loads(manifest_bytes)
    require(manifest["repository"] == REPOSITORY and manifest["distribution"] is True
            and manifest["tag"] == tag and manifest["version"] == version,
            "Unexpected release manifest")
    require(re.fullmatch(r"[a-f0-9]{40}", manifest["commit"]), "Invalid source commit")
    # Fail closed if any declared platform is incomplete.
    files = {f["file"]: f for f in manifest["files"]}
    for name, entry in files.items():
        published = assets[name]
        require(published["state"] == "uploaded" and published["size"] == entry["bytes"]
                and published["digest"] == "sha256:" + entry["sha256"], f"Incomplete release: {name}")
    for download in manifest["downloads"].values():
        entry = files[download["file"]]
        require(download["sha256"] == entry["sha256"] and download["bytes"] == entry["bytes"]
                and download["url"] == f"{BASE}/download/{tag}/{download['file']}", "Invalid download")
    download = manifest["downloads"]["macos-arm64"]
    filename = f"Monoprint-{version}-aarch64-apple-darwin.zip"
    require(download["file"] == filename, "Unexpected macOS archive")
    require("appcast-macos-arm64.xml" in files, "Missing Sparkle feed")
    current = CASK.read_text()
    old_version = re.search(r'  version "([^"]+)"', current).group(1)
    old_sha = re.search(r'  sha256 "([^"]+)"', current).group(1)
    require(tuple(map(int, version.split('.'))) >= tuple(map(int, old_version.split('.'))),
            "Refusing to downgrade the cask")
    require(version != old_version or download["sha256"] == old_sha,
            "Published version changed bytes; refusing replacement")

    with tempfile.TemporaryDirectory(prefix="monoprint-cask-") as directory:
        root = Path(directory)
        (root / filename).write_bytes(asset(filename))
        (root / "release.json").write_bytes(manifest_bytes)
        bundle = root / "provenance.sigstore.json"
        bundle.write_bytes(asset(bundle.name))
        for name in [filename, "release.json"]:
            subprocess.run([
                "gh", "attestation", "verify", str(root / name), "--repo", REPOSITORY,
                "--bundle", str(bundle), "--signer-workflow",
                f"{REPOSITORY}/.github/workflows/desktop-release.yml",
                "--source-digest", manifest["commit"], "--source-ref", f"refs/tags/{tag}",
                "--deny-self-hosted-runners",
            ], check=True)

    updated = current.replace(f'  version "{old_version}"', f'  version "{version}"')
    updated = updated.replace(f'  sha256 "{old_sha}"', f'  sha256 "{download["sha256"]}"')
    CASK.write_text(updated)
    print(f"Verified Monoprint {version}" + ("; cask updated" if updated != current else "; cask current"))


if __name__ == "__main__":
    main()
