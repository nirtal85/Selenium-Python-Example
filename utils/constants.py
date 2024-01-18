from pathlib import Path


class Constants:
    AUTOMATION_USER_AGENT = "automation"
    DATA_PATH = Path(Path(__file__).absolute().parent.parent, "data")
