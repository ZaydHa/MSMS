import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
import shutil

def init_logger(log_file: str = "msms.log") -> None:
    """Initialize application-wide logging (idempotent)."""
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    fh = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)

    root.addHandler(ch)
    root.addHandler(fh)
    logging.info("Logger initialized.")

def backup_data(data_path: str = "msms.json", backup_dir: str = "backups") -> str:
    """Copy data file to a timestamped backup in backup_dir; returns backup path or ''."""
    src = Path(data_path)
    Path(backup_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = Path(backup_dir) / f"{src.stem}_{ts}{src.suffix}"
    if src.exists():
        shutil.copy2(src, dst)
        logging.info(f"Data backup created: {dst}")
        return str(dst)
    logging.warning(f"No data file to back up at {src.resolve()}")
    return ""
