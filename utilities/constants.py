from pathlib import Path


class Constants:
    AUTOMATION_USER_AGENT: str = "automation"
    DATA_PATH: Path = Path(Path(__file__).absolute().parent.parent, "data")
    CHROME_DOWNLOAD_DIRECTORY: Path = DATA_PATH / "downloads"
    DIFF_TOLERANCE_PERCENT: float = 0.01
