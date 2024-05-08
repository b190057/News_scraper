import logging.config
from pathlib import Path
import yaml

from config.logger.handlers import create_log_folder, get_os_architecture


def config_logging(log_type: str="_scraper", filename: str="scraper_log") -> None:
    """
    Configures logging library.
    It loads the YAML file on the project that establishes the different loggers and their handlers.

    Args:
        log_type (str, optional): establish the configuration file type. Defaults to "_scraper".
        filename (str, optional): establish the personalized log filename. Defaults to "scraper_log".
    """
    os = get_os_architecture()[0]

    file_path_config = Path(__file__).parent.joinpath(f'logger_{os}{log_type}.yml')
    print("Logger: ", file_path_config)
    with open(file_path_config, 'r') as file:
        create_log_folder(filename=filename + '.log')

        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
