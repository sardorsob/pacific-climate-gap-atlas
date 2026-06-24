"""Project path helpers."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTEXT = ROOT / "context"
RESEARCH = ROOT / "research"
DATA = ROOT / "data"
ARTIFACTS = ROOT / "artifacts"
CONFIGS = ROOT / "configs"


def project_path(*parts: str) -> Path:
    """Build an absolute path inside the repository."""

    return ROOT.joinpath(*parts)
