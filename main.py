import sqlite3
from sqlite3 import Error
import shutil
import os
import re
import glob
"""
PLAN:
create connection -> connect to db -> create tables if not exists
get files from input folder to list -> parse it to variables -> variables load to db into appropriate tables 

"""
#TODO: Logging
#TODO: parse file into variables:
#                   book_name,
#                   number_of_paragraphs,
#                   number_of_words,
#                   number_of_letters,
#                   words_with_capital_letters,
#                   words_in_lowercase
#TODO: create table for each new file with fields/variables:
#                   word, count, count_uppercase


file_template = "input/*.txt"
path_for_incorrect_files = "incorrect_input"


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_statement_sql):
    try:
        c = conn.cursor()
        c.execute(create_statement_sql)
    except Error as e:
        print(e)

#def move_files


def main():
    database = "monitorapp.db"
    sql_create_table_common = """CREATE TABLE IF NOT EXISTS common_files_info (
                                    book_name text PRIMARY KEY,
                                    number_of_paragraphs int,
                                    number_of_words int,
                                    number_of_letters int,
                                    words_with_capital_letters int,
                                    words_in_lowercase int);
    """
    sql_create_table_for_each_file = """ 
    """



list_of_files = []
for file in glob.glob(file_template):
    list_of_files.append(file)


if __name__ == '__main__':
    print(list_of_files)
    for file in list_of_files:
        shutil.move(file, path_for_incorrect_files)
