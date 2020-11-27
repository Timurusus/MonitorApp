import sqlite3
from sqlite3 import Error
import shutil
import glob
from xml.dom import minidom
import logging
import os
from datetime import datetime


file = "input/*.fb2"
path_for_incorrect_files = "incorrect_input/"
values_for_file_table = dict()


def get_book_name_from_fb2(path_to_file):
    xml_doc = minidom.parse(path_to_file)
    book_name = xml_doc.getElementsByTagName("book-title")[0].firstChild.data
    return book_name


def get_number_of_paragraphs_from_fb2(path_to_file):
    xml_doc = minidom.parse(path_to_file)
    tags = xml_doc.getElementsByTagName("p")
    return len(tags)


def get_number_of_words_from_fb2(path_to_file):
    return len(return_list_of_words(path_to_file=path_to_file))


def return_list_of_words(path_to_file):
    xml_doc = minidom.parse(path_to_file)
    tags = xml_doc.getElementsByTagName("p")
    list_of_words = []
    for p in tags:
        for i in p.childNodes:
            list_of_words = list_of_words + (str(i.nodeValue).split())
    return list_of_words


def populate_dict_of_count_words(path_to_file):
    d = {}
    words = return_list_of_words(path_to_file=path_to_file)
    for word in words:
        if word.lower() in d:
            if any(i.isupper() for i in word):
                d[word.lower()][1] = d[word.lower()][1] + 1
            d[word.lower()][0] = d[word.lower()][0] + 1
        else:
            if any(i.isupper() for i in word):
                d[word.lower()] = [1, 1]
            else:
                d[word.lower()] = [1, 0]
    return d


def return_number_of_letters(path_to_file):
    count = 0
    for word in return_list_of_words(path_to_file=path_to_file):
        count += len(word)
    return count


def return_number_of_words_with_lowercase(path_to_file):
    count = 0
    for word in return_list_of_words(path_to_file=path_to_file):
        if word.islower():
            count += 1
    return count


def return_number_of_words_with_capital_letters(path_to_file):
    count = 0
    for word in return_list_of_words(path_to_file=path_to_file):
        if any(x.isupper() for x in word):
            count += 1
    return count


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
    sql_insert_into_common_table_info = "INSERT INTO common_files_info VALUES (?,?,?,?,?,?)"

    conn = create_connection(database)
    create_table(conn=conn, create_statement_sql=sql_create_table_common)
    conn.commit()

    list_of_files = get_file_names_to_list(file_temp=file)
    if list_of_files:
        for fi in list_of_files:
            dict_for_common_files_info_table = get_values_for_common_files_info_table(file_temp=fi)
            conn.execute(sql_insert_into_common_table_info, (dict_for_common_files_info_table["book_name"],
                                                             dict_for_common_files_info_table["number_of_paragraphs"],
                                                             dict_for_common_files_info_table["number_of_words"],
                                                             dict_for_common_files_info_table["number_of_letters"],
                                                             dict_for_common_files_info_table["words_with_capital_letters"],
                                                             dict_for_common_files_info_table["words_in_lowercase"]))
            conn.commit()
            cur = conn.cursor()
            table_name = fi[6:-4]
            cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (word text, count int, count_uppercase int);")
            conn.commit()
            for k, v in populate_dict_of_count_words(fi).items():
                conn.execute(f"INSERT INTO {table_name} VALUES (?,?,?)", (k, v[0], v[1]))
            conn.commit()
    else:
        print("Files with .fb2 extension are absent.")
    conn.close()


def get_file_names_to_list(file_temp):
    list_of_files = []
    for file_name in glob.glob(file_temp):
        list_of_files.append(file_name)
    return list_of_files


def move_files(archive, path_for_incorrect):
    for f in glob.glob("input/*"):
        if f.endswith(".fb2"):
            shutil.move(f, archive)
            LOGGER.info("File {f} is moved to archive.".format(f=f))
        else:
            shutil.move(f, path_for_incorrect)
            LOGGER.info("File {f} is moved to incorrect_input.".format(f=f))


def get_values_for_common_files_info_table(file_temp):
    values_for_common_files_info_table = {}
    book_name = get_book_name_from_fb2(file_temp)
    number_of_paragraphs = get_number_of_paragraphs_from_fb2(file_temp)
    number_of_words = get_number_of_words_from_fb2(file_temp)
    number_of_letters = return_number_of_letters(file_temp)
    words_with_capital_letters = return_number_of_words_with_capital_letters(file_temp)
    words_in_lowercase = return_number_of_words_with_lowercase(file_temp)
    values_for_common_files_info_table['book_name'] = book_name
    values_for_common_files_info_table['number_of_paragraphs'] = number_of_paragraphs
    values_for_common_files_info_table['number_of_words'] = number_of_words
    values_for_common_files_info_table['number_of_letters'] = number_of_letters
    values_for_common_files_info_table['words_with_capital_letters'] = words_with_capital_letters
    values_for_common_files_info_table['words_in_lowercase'] = words_in_lowercase
    return values_for_common_files_info_table


if __name__ == '__main__':
    start_dt = datetime.now()
    LOG_FILE_PATH = "log_file.txt"
    logging.basicConfig(filename=LOG_FILE_PATH,
                        format='%(asctime)s %(message)s',
                        filemode='w')
    LOGGER = logging.getLogger("MonitorApp")
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.info("Start of the MonitorApp.")
    main()
    LOGGER.info("Starting of moving files from input folder: {}".format(datetime.now()))
    move_files("archive/", path_for_incorrect_files)
    LOGGER.info("End of moving files from input folder: {}".format(datetime.now()))
    diff_dt = datetime.now() - start_dt
    LOGGER.info("MonitorApp runtime is: {}".format(diff_dt))
