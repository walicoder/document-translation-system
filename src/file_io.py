from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def read_text_from_txt(file_path: str | Path) -> str:
    """Read text from files
    """
    with open(file_path) as f:
        contents = f.read()
        logger.info(f"File read successfully from {file_path}")
        return contents


