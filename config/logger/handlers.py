import os
from config.constants import LOG_FOLDER_PATH

import platform
import struct


def create_log_folder(filename: str="scraper_log.log") -> None:
    """Creates the folder log and the file if they don't exist.

    Args:
        filename (str, optional): file name to store the logs. Defaults to "scraper_log.log".
    """

    os.makedirs(LOG_FOLDER_PATH, exist_ok=True)
    log_path = os.path.join(LOG_FOLDER_PATH, filename)
    os.path.exists(log_path) or open(log_path, 'w').close()


def get_os_architecture() -> tuple[str, int]:
    """
    Obtains the name of the Operation System and the architecture (32 or 64 bits) where the software is
    being executed in lower case.

    Returns:
        tuple[str, int]: Operative System and architecture values as tuple
    """

    return platform.system().lower(), struct.calcsize('P') * 8
