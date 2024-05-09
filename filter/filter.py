# implement filter operations
from filter import logger
from config.constants import CSV_FILENAME, DATA_PATH, QUESTION_1, QUESTION_2, ANSWER_FILENAME
from config.msg import ERROR_ANSWER_1, ERROR_ANSWER_2, ERROR_COMBINING_ANSWERS, ERROR_CLEANING_DATA, ERROR_PARSING

import os
import re

import pandas as pd


def parse_number(text: str) -> int:
    """get the first appearance of a number from a given text

    Args:
        text (str): string to obtain the number from

    Returns:
        int: the first appearance of a number
    """
    answer = None
    try:
        match = re.search(r'\d+', text)
        if match:
            answer = int(match.group())

    except:
        logger.error(ERROR_PARSING)

    return answer


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset

    Args:
        df (pd.DataFrame): Original dataframe obtained from the scraper

    Returns:
        pd.DataFrame: Eliminate null values
    """
    try:
        df = df.dropna(subset=['title'])
    except:
        logger.error(ERROR_CLEANING_DATA)

    return df


def answer_first_question(df: pd.DataFrame) -> str:
    """Answer the first question:{question}

    Args:
        df (pd.DataFrame): dataframe with non null titles

    Returns:
        str: Answer to the first question
    """.format(question=QUESTION_1)
    answer = ""
    try:
        df_aux = df.dropna(subset=['n_comments'])
        df_aux['n_comments'] = df_aux['n_comments'].apply(lambda x: parse_number(str(x)))
        df_aux = df_aux[df_aux['title'].apply(lambda x: len(x.split()) > 5)].sort_values(by='n_comments', ascending=False)
        answer = df_aux.dropna(subset=['n_comments'])
    except:
        logger.error(ERROR_ANSWER_1)
    
    return answer


def answer_second_question(df: pd.DataFrame) -> str:
    """Answer the second question:{question}

    Args:
        df (pd.DataFrame): dataframe with non null titles

    Returns:
        str: Answer to the second question
    """.format(question=QUESTION_2)
    answer = ""
    try:
        df_aux = df.dropna(subset=['points'])
        df_aux['points'] = df_aux['points'].apply(lambda x: parse_number(str(x)))
        df_aux = df_aux[df_aux['title'].apply(lambda x: len(x.split()) <= 5)].sort_values(by='points', ascending=False)
        answer = df_aux.dropna(subset=['points'])
    except:
        logger.error(ERROR_ANSWER_2)
    
    return answer


def save_answers(answer1: str, answer2:str) -> None:
    """Combines the questions with the answers and save them into a txt file

    Args:
        answer1 (str): answer for the first question
        answer2 (str): answer for the second question
    """
    try:
        combine_questions_answers = QUESTION_1 + "\n"+ str(answer1) + "\n" + QUESTION_2 + "\n"+ str(answer2)
        logger.info(f"Final answer: {combine_questions_answers}")
        with open(os.path.join(DATA_PATH, ANSWER_FILENAME), "w") as archivo:
            archivo.write(combine_questions_answers)
    except:
        logger.error(ERROR_COMBINING_ANSWERS)


def answer_questions() -> None:
    """Answer the two questions provided
    """
    df = pd.read_csv(os.path.join(DATA_PATH, CSV_FILENAME))
    df = clean_df(df)
    answer1 = answer_first_question(df)
    answer2 = answer_second_question(df)
    save_answers(answer1, answer2)
