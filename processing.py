# import xml.etree.ElementTree as ET
from xml.dom import minidom

# tree = ET.parse('Example.fb2')
# root = tree.getroot()
# book_name = root[0][0][3].text
# print(book_name)

#'Example.fb2'


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



# print(get_number_of_words_from_fb2('Example.fb2'))

print(return_number_of_words_with_capital_letters('Example.fb2'))

