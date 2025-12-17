from pathlib import Path


def project_root() -> Path:
    """
    Returns the project root folder:
    .../cs2-demo-analyzer

    Assumes this file lives at:
    .../cs2-demo-analyzer/src/util/paths.py
    """
    return Path(__file__).resolve().parents[2]


def outputs_awpy_dir() -> Path:
    return project_root() / "outputs" / "awpy"
