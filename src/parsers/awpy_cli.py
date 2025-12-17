import subprocess
import zipfile
from pathlib import Path
from datetime import datetime

from util.paths import project_root, outputs_awpy_dir


def _log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def parse_demo_to_folder(demo_path: str) -> Path:
    """
    Runs: awpy parse <demo>
    - Executes in PROJECT_ROOT so the .zip lands where we expect
    - Extracts to outputs/awpy/<demo_stem>/
    - Moves the .zip into outputs/awpy/ as an artifact
    - Returns the parsed folder path
    """
    demo = Path(demo_path)
    if not demo.exists():
        raise FileNotFoundError(f"Demo not found: {demo}")

    root = project_root()
    out_dir = outputs_awpy_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    zip_name = f"{demo.stem}.zip"
    zip_path = root / zip_name

    # Remove old zip to avoid confusion
    if zip_path.exists():
        zip_path.unlink()

    _log(f"Parsing demo with awpy: {demo}")
    result = subprocess.run(
        ["awpy", "parse", str(demo)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        _log("awpy parse failed.")
        if result.stdout:
            _log("STDOUT:\n" + result.stdout)
        if result.stderr:
            _log("STDERR:\n" + result.stderr)
        raise RuntimeError("awpy parse failed (see logs above).")

    if not zip_path.exists():
        raise RuntimeError(f"Expected zip not found at: {zip_path}")

    parsed_folder = out_dir / demo.stem
    parsed_folder.mkdir(parents=True, exist_ok=True)

    _log(f"Extracting: {zip_path.name} -> {parsed_folder}")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(parsed_folder)

    # Keep the zip as an artifact in outputs/awpy/
    zip_copy = out_dir / zip_name
    if zip_copy.exists():
        zip_copy.unlink()
    zip_path.replace(zip_copy)

    return parsed_folder
