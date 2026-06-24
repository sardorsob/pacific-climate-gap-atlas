"""Profile official datasets for coverage, years, and missingness."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.io.dataset_profile import (  # noqa: E402
    DatasetProfile,
    error_profile,
    profile_csv_text,
    profile_to_contract,
    profile_to_csv_row,
)
from analysis.io.official_data import OfficialDataset, read_official_inventory  # noqa: E402


DEFAULT_CONFIG = ROOT / "configs" / "datasets.yml"
DEFAULT_OUTPUT = ROOT / "artifacts" / "tables" / "dataset_profile.csv"
DEFAULT_CONTRACTS_DIR = ROOT / "data" / "contracts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to dataset profiling config.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path for the profile CSV artifact.",
    )
    parser.add_argument(
        "--contracts-dir",
        type=Path,
        default=DEFAULT_CONTRACTS_DIR,
        help="Directory for per-dataset JSON contracts.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds for each SDMX CSV request.",
    )
    return parser.parse_args()


def load_config(path: Path) -> dict[str, object]:
    config: dict[str, object] = {}
    section: str | None = None
    current_dataset: dict[str, str] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if not raw_line.startswith(" "):
            if current_dataset is not None:
                config.setdefault("priority_datasets", []).append(current_dataset)
                current_dataset = None

            key, _, value = stripped.partition(":")
            section = key if not value.strip() else None
            if value.strip():
                config[key] = value.strip()
            elif key == "priority_datasets":
                config[key] = []
            continue

        if section != "priority_datasets":
            continue

        if stripped.startswith("- "):
            if current_dataset is not None:
                config.setdefault("priority_datasets", []).append(current_dataset)
            current_dataset = {}
            stripped = stripped[2:].strip()

        if current_dataset is not None and ":" in stripped:
            key, _, value = stripped.partition(":")
            current_dataset[key.strip()] = value.strip()

    if current_dataset is not None:
        config.setdefault("priority_datasets", []).append(current_dataset)

    if "priority_datasets" not in config:
        raise ValueError(f"{path} is missing `priority_datasets`.")

    return config


def profile_priority_datasets(
    *,
    config: dict[str, object],
    timeout: float,
) -> list[DatasetProfile]:
    inventory_path = ROOT / str(config.get("official_inventory", "research/official_datasets_2026.csv"))
    accept_header = str(
        config.get("api_accept_header", "application/vnd.sdmx.data+csv;version=2.0")
    )
    inventory = {dataset.name: dataset for dataset in read_official_inventory(inventory_path)}

    profiles: list[DatasetProfile] = []
    for entry in config["priority_datasets"]:
        if not isinstance(entry, dict):
            raise ValueError("Each priority dataset entry must be a mapping.")

        name = str(entry["name"])
        pillar = str(entry["pillar"])
        inventory_row = inventory.get(name)
        if inventory_row is None:
            profiles.append(
                error_profile(
                    name=name,
                    pillar=pillar,
                    story_role="",
                    official_url="",
                    sdmx_csv_api_url="",
                    status="missing_inventory_row",
                    caveat_notes="Dataset is listed in config but not found in official inventory.",
                )
            )
            continue

        profiles.append(
            profile_inventory_row(
                inventory_row=inventory_row,
                pillar=pillar,
                accept_header=accept_header,
                timeout=timeout,
            )
        )

    return profiles


def profile_inventory_row(
    *,
    inventory_row: OfficialDataset,
    pillar: str,
    accept_header: str,
    timeout: float,
) -> DatasetProfile:
    if not inventory_row.sdmx_csv_api_url:
        return error_profile(
            name=inventory_row.name,
            pillar=pillar,
            story_role=inventory_row.story_role,
            official_url=inventory_row.official_url,
            sdmx_csv_api_url="",
            status="no_api_url",
            caveat_notes="Official inventory has no SDMX CSV API URL.",
        )

    csv_text, error_status, caveat_notes = fetch_sdmx_csv_text(
        url=inventory_row.sdmx_csv_api_url,
        accept_header=accept_header,
        timeout=timeout,
    )
    if error_status:
        return error_profile(
            name=inventory_row.name,
            pillar=pillar,
            story_role=inventory_row.story_role,
            official_url=inventory_row.official_url,
            sdmx_csv_api_url=inventory_row.sdmx_csv_api_url,
            status=error_status,
            caveat_notes=caveat_notes,
        )

    return profile_csv_text(
        name=inventory_row.name,
        pillar=pillar,
        story_role=inventory_row.story_role,
        official_url=inventory_row.official_url,
        sdmx_csv_api_url=inventory_row.sdmx_csv_api_url,
        csv_text=csv_text or "",
    )


def fetch_sdmx_csv_text(
    *,
    url: str,
    accept_header: str,
    timeout: float,
) -> tuple[str | None, str | None, str]:
    """Fetch SDMX CSV text, using PowerShell fallback for picky Windows endpoint behavior."""

    headers = {
        "Accept": accept_header,
        "User-Agent": "pacific-climate-gap-atlas/0.1 dataset-profiler",
    }
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            status_code = response.getcode()
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
    except HTTPError as exc:
        if exc.code == 422:
            fallback_text = fetch_with_powershell(url=url, accept_header=accept_header, timeout=timeout)
            if fallback_text is not None:
                return fallback_text, None, ""
        return None, f"api_error_{exc.code}", f"SDMX CSV API returned HTTP {exc.code}."
    except (OSError, URLError) as exc:
        fallback_text = fetch_with_powershell(url=url, accept_header=accept_header, timeout=timeout)
        if fallback_text is not None:
            return fallback_text, None, ""
        return None, "fetch_error", f"Could not fetch SDMX CSV API response: {exc}"

    if status_code != 200:
        return None, f"api_error_{status_code}", f"SDMX CSV API returned HTTP {status_code}."

    return body.decode(charset, errors="replace"), None, ""


def fetch_with_powershell(*, url: str, accept_header: str, timeout: float) -> str | None:
    """Fetch through Windows PowerShell when the SDMX endpoint rejects urllib requests."""

    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if powershell is None:
        return None

    timeout_seconds = max(1, int(timeout))
    script = "\n".join(
        [
            "$ErrorActionPreference = 'Stop'",
            "$headers = @{ Accept = " + _ps_single_quote(accept_header) + " }",
            "$response = Invoke-WebRequest -UseBasicParsing "
            + "-Uri "
            + _ps_single_quote(url)
            + " -Headers $headers -Method Get -TimeoutSec "
            + str(timeout_seconds),
            "if ($response.Content -is [byte[]]) {",
            "  [Console]::OutputEncoding = [Text.Encoding]::UTF8",
            "  [Console]::Write([Text.Encoding]::UTF8.GetString($response.Content))",
            "} else {",
            "  [Console]::OutputEncoding = [Text.Encoding]::UTF8",
            "  [Console]::Write([string]$response.Content)",
            "}",
        ]
    )

    result = subprocess.run(
        [powershell, "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout + 10,
        check=False,
    )
    if result.returncode != 0:
        return None

    return result.stdout


def _ps_single_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def write_outputs(
    *,
    profiles: list[DatasetProfile],
    output_path: Path,
    contracts_dir: Path,
    generated_at_utc: str,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    contracts_dir.mkdir(parents=True, exist_ok=True)

    rows = [profile_to_csv_row(profile, generated_at_utc=generated_at_utc) for profile in profiles]
    pd.DataFrame(rows).to_csv(output_path, index=False)

    for profile in profiles:
        contract = profile_to_contract(profile, generated_at_utc=generated_at_utc)
        contract_path = contracts_dir / f"{profile.slug}.json"
        contract_path.write_text(
            json.dumps(contract, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )


def print_summary(profiles: list[DatasetProfile], output_path: Path, contracts_dir: Path) -> None:
    ok_count = sum(1 for profile in profiles if profile.status == "ok")
    print(f"Profiled {len(profiles)} priority datasets ({ok_count} ok).")
    print(f"Wrote profile table: {output_path}")
    print(f"Wrote contracts: {contracts_dir}")

    for profile in profiles:
        years = (
            ""
            if profile.year_start is None or profile.year_end is None
            else f"{profile.year_start}-{profile.year_end}"
        )
        print(
            f"- {profile.name}: {profile.status}, rows={profile.row_count}, "
            f"geographies={profile.geography_count}, years={years}"
        )


def main() -> int:
    args = parse_args()
    config_path = ROOT / args.config if not args.config.is_absolute() else args.config
    output_path = ROOT / args.output if not args.output.is_absolute() else args.output
    contracts_dir = ROOT / args.contracts_dir if not args.contracts_dir.is_absolute() else args.contracts_dir

    config = load_config(config_path)
    profiles = profile_priority_datasets(config=config, timeout=args.timeout)
    generated_at_utc = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    write_outputs(
        profiles=profiles,
        output_path=output_path,
        contracts_dir=contracts_dir,
        generated_at_utc=generated_at_utc,
    )
    print_summary(profiles, output_path, contracts_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
