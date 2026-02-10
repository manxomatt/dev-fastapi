import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging(log_file: str = "logs/app.log") -> None:
    """Configure root logger: separate handlers for info (success) and error (fail)."""
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    # ensure log directory exists
    log_path = Path(log_file).parent
    if not log_path.exists():
        os.makedirs(log_path, exist_ok=True)

    # Info handler (success / access)
    info_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    # Error handler (failed requests / exceptions)
    error_handler = RotatingFileHandler(log_file.replace(".log", ".err.log"), maxBytes=5_000_000, backupCount=3)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    root = logging.getLogger()
    # Avoid duplicating handlers if called multiple times
    if not any(isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", "") == info_handler.baseFilename for h in root.handlers):
        root.setLevel(logging.INFO)
        root.addHandler(info_handler)
        root.addHandler(error_handler)
