import sqlite3
from sqlite3 import Error
import shutil
import glob
from xml.dom import minidom

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


# file = "input/*.fb2"
file = "input/Example.fb2"
path_for_incorrect_files = "incorrect_input"
list_of_files = []
values_for_common_files_info_table = dict()


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
    sql_insert_into_common_table_info = "INSERT INTO common_files_info VALUES (?,?,?,?,?,?)"

    conn = create_connection(database)
    create_table(conn=conn, create_statement_sql=sql_create_table_common)
    conn.commit()
    get_values_for_common_files_info_table(file_temp=file)
    conn.execute(sql_insert_into_common_table_info, (values_for_common_files_info_table["book_name"],
                                                     values_for_common_files_info_table["number_of_paragraphs"],
                                                     values_for_common_files_info_table["number_of_words"],
                                                     values_for_common_files_info_table["number_of_letters"],
                                                     values_for_common_files_info_table["words_with_capital_letters"],
                                                     values_for_common_files_info_table["words_in_lowercase"]))
    conn.commit()
    conn.close()



    sql_create_table_for_each_file = """ 
    """


def get_file_names_to_list(file_temp):
    for file_name in glob.glob(file_temp):
        list_of_files.append(file_name)
    return list_of_files


def move_files(files, path_for_incorrect):
    for file in files:
        shutil.move(file, path_for_incorrect)


def get_values_for_common_files_info_table(file_temp):
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





if __name__ == '__main__':
    # main()
    conn = create_connection("monitorapp.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM common_files_info")
    res = cur.fetchall()
    print(res)