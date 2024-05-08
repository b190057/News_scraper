from config.logger import config_logging
from scraper.scraper import Scraper

from config.constants import SCRAPER_LOG_CONFIG, SCRAPER_LOG_FILENAME


def main() -> None:
    """Initilize the log and start the scraper
    """
    config_logging(log_type=SCRAPER_LOG_CONFIG, filename=SCRAPER_LOG_FILENAME)
    scraper = Scraper()
    scraper.start_scraper()


if __name__ == "__main__":
    main()
