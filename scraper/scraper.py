from scraper import logger
import os
import time
import pandas as pd

import bs4
from bs4 import BeautifulSoup
from selenium import webdriver

from config.constants import MAIN_WEBPAGE, DATA_PATH, CSV_FILENAME
from config.msg import ERROR_INITIALIZATION, ERROR_GENERATING_CSV, ERROR_ROWS_NOT_FOUND, ERROR_FINDING_SCORE, \
    ERROR_FINDING_COMMENTS, ERROR_FINDING_RANK, ERROR_FINDING_SIBLING, ERROR_FINDING_TITLE, SUCCESS_GENERATING_CSV


class Scraper:
    def __init__(self):
        pass

    def initialize_driver(self) -> webdriver:
        """
        Gets into the news webpage

        Returns:
            webdriver: Returns the firefox driver of the webpage
        """
        driver = None
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-cookies")
            driver = webdriver.Firefox(options=options)

            # Get into the main webpage
            driver.get(MAIN_WEBPAGE)
            time.sleep(3)
        except:
            logger.error(ERROR_INITIALIZATION.format(webpage=MAIN_WEBPAGE))

        return driver
    

    def get_data(self, soup: bs4.BeautifulSoup) -> pd.DataFrame:
        """Get the information extracted for each row

        Args:
            soup (bs4.BeautifulSoup): soup containing the HTML information of the webpage

        Returns:
            pd.DataFrame: Panda's dataframe containing all the information
        """

        df = pd.DataFrame(columns=['title', 'n_order', 'n_comments', 'points'])
        rows = soup.find_all('tr', class_='athing')

        if not rows:
            logger.error(ERROR_ROWS_NOT_FOUND)
            return df
        
        for row in rows:

            # Get rank
            rank = row.find('span', class_='rank')
            if rank:
                rank = rank.text.strip()
            else:
                logger.error(ERROR_FINDING_RANK)
                rank = None

            # Get title
            title_aux = row.find_all('td', class_='title')
            title = None
            for item in title_aux:
                # if we find the title, do not contiue checkin
                if title:
                    break
                if item.find('a'):
                    title = item.find('a').text.strip()
            
            if not title:
                logger.error(ERROR_FINDING_TITLE)

            # get the sibling to obtain the score and the number of comments
            sibling = row.find_next_sibling()
            if not sibling:
                logger.error(ERROR_FINDING_SIBLING)
                continue

            # Get score
            score = sibling.find('span', class_='score')
            if score:
                score = score.text.strip()
            else:
                logger.error(ERROR_FINDING_SCORE)
                score = None

            # Get number of comments
            comment_aux = sibling.find_all('a')
            comment = None
            for item in comment_aux:
                if 'comment' in item.text:
                    comment = item.text.strip()

            if comment is None:
                logger.error(ERROR_FINDING_COMMENTS)
            
            df = df._append({'title': title, 'n_order': rank, 'n_comments': comment, 'points': score}, ignore_index=True)

        return df
    

    def get_news(self,driver: webdriver) -> None:
        """
        Generates a csv file with the information of each row

        Args:
            driver (webdriver): Driver containing the main webpage
        """

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        df = None

        try:
            df = self.get_data(soup)
            df.to_csv(os.path.join(DATA_PATH, CSV_FILENAME), index=False)
            logger.info(SUCCESS_GENERATING_CSV)
        except Exception as e:
            logger.error(f"{ERROR_GENERATING_CSV}: {e}")


    def start_scraper(self):
        """Initialize the webdriver and starts the scraper
        """
        driver = self.initialize_driver()
        if driver:
            self.get_news(driver)
            driver.close()
