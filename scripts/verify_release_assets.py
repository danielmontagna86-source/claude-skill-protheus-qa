"""Read back published GitHub assets and require matching commit, names, size and SHA256."""
import argparse
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen
from tirqa_core import digest, require, write_json, parse_json
from verify_distribution import verify_archive


def verify_metadata(metadata: dict, repo: str, tag: str, commit: str, files: list[Path]) -> list[tuple[Path, str]]:
    require(metadata.get("tag_name") == tag and metadata.get("target_commitish") == commit
            and metadata.get("draft") is False and metadata.get("prerelease") is True,
            "release_target_mismatch")
    assets = metadata.get("assets", [])
    require(isinstance(assets, list), "assets_missing")
    by_name = {a["name"]: a for a in assets}
    require(len(by_name) == len(assets), "duplicate_assets")
    result = []
    for path in files:
        require(path.name in by_name, "release_asset_missing")
        asset = by_name[path.name]; data = path.read_bytes()
        expected_url = f"https://github.com/{repo}/releases/download/{tag}/{path.name}"
        require(asset.get("state") == "uploaded" and asset.get("size") == len(data)
                and asset.get("digest") == "sha256:" + digest(data)
                and asset.get("browser_download_url") == expected_url, "release_asset_mismatch")
        result.append((path, expected_url))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True); parser.add_argument("--tag", required=True)
    parser.add_argument("--commit", required=True); parser.add_argument("--files", nargs="+", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo), "invalid_repository")
    require(re.fullmatch(r"v\d+\.\d+\.\d+-rc\.\d+", args.tag), "invalid_tag")
    require(re.fullmatch(r"[a-f0-9]{40}", args.commit), "invalid_commit")
    url = f"https://api.github.com/repos/{args.repo}/releases/tags/{args.tag}"
    with urlopen(Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "protheus-qa-release-check"}), timeout=30) as response:
        metadata = parse_json(response.read(2_000_001))
    checked = {}
    for path, url in verify_metadata(metadata, args.repo, args.tag, args.commit, args.files):
        with urlopen(url, timeout=60) as response:
            data = response.read(20_000_001)
        require(data == path.read_bytes(), "downloaded_asset_mismatch")
        if path.name.endswith(".zip"): verify_archive(data)
        checked[path.name] = digest(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {"status": "PUBLISHED_ASSETS_VERIFIED", "tag": args.tag, "commit": args.commit,
              "files": checked, "erp_validated": False}
    write_json(args.output, report); print(json.dumps(report, indent=2))


if __name__ == "__main__": main()
