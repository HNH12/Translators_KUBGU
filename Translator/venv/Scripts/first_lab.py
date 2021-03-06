import re

# True - если найдено совпадение word с элементом из списка разделителей
def is_separator(word):
    return (
        word in (';', '{', '}', '(', ')', ',', '[', ']')
    )

# True - если найдено совпадение word с элементом из списка односоставных типов
def is_simple_variable_type(word):
    return (
        word in ('short', 'char', 'int', 'signed', 'unsigned',
                 'long', 'float', 'double', 'void')
    )

# True - если найдено совпадение word с элементом из списка сложных типов
def is_composite_variable_type(word):
    return (
        word in ('signed char', 'unsigned char', 'short int',
                  'signed short', 'signed short', 'unsigned short',
                  'signed int', 'unsigned int', 'long int', 'long long',
                  'signed long', 'long double')
    )

# True - если найдено совпадение word с элементом из списка служебных слов
def is_special_words(word):
    return (
        word in ('while', 'for', 'if', 'else', 'switch', 'case', 'goto', 'break',
                 'static', 'printf', 'scanf', 'return', 'continue', 'getch', 'malloc', 'new')
    )

# True - если найдено совпадение word с элементом из списка операций
def is_operator(word):
    return (
        word in ('=', '!', '<', '>', '+', '-', '/', '%', '*', '$', '~', '&', '|', '+')
    )

# Добавляет new_elem в словарь dictionary, если new_elem отсуствует в указанном dictionary
def check(key, dictionary, new_elem):
    if new_elem not in dictionary[key]:
        dictionary[key][new_elem] = len(dictionary[key]) + 1

# Возвращает пару ключ-значение
def return_from_dictionary(key, dictionary, word):
    elem = dictionary[key]
    number = elem[word]
    return "{0}{1}".format(key,number)

# True - если переданная строка является числом
def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

# True - если переданная строка является константой строкового типа
def is_str(word):
    if word[0] == "'" or word[0] == '"':
        return True
    return False


def is_m(str):
    if str.find('М') != -1:
        return True
    return False


def is_func(str):
    if str.find('Ф') != -1:
        return True
    return False


def is_aem(str):
    if str.find('АЭМ') != -1:
        return True
    return False


# def get_paramaters_start_function(dictionary, word):
#     class_lexem = word[0]
#     number = word[1:]
#     return dictionary[class_lexem][number]


# вывод словаря в файл
def output_table(class_lit):
    text = str()
    if class_lit == 'W':
        text += 'Специальные слова' + '\n'
    elif class_lit == 'I':
        text += 'Идентификаторы' + '\n'
    elif class_lit == 'O':
        text += 'Операции' + '\n'
    elif class_lit == 'R':
        text += 'Разделители' + '\n'
    elif class_lit == 'N':
        text += 'Числовые константы' + '\n'
    else:
        text += 'Символьные константы' + '\n'
    text += 'Лексема\tКод'
    return text

# Сканер лексического анализатора
def scan(text):
    dictionary = {'W':{}, 'I':{}, 'O':{}, 'R':{}, 'N':{}, 'C':{}}

    list_symb = list()
    for line in text:
        word = ''
        check_str = False

        for i in range(len(line)):

            if not(check_str) and (line[i] == ' ' or is_separator(line[i]) or is_operator(line[i])) and len(line[i]) != 0:

                check_i = True
                check_const = False

                if not(is_simple_variable_type(word)) and word!='' and not(is_special_words(word)):
                    if is_number(word) and not(check_const):
                        check_const = True
                        check_i = False
                        check('N', dictionary, word)
                        list_symb.append(return_from_dictionary('N', dictionary, word))

                    if is_str(word) and not(check_const):
                        check_i = False
                        check('C', dictionary, word)
                        list_symb.append(return_from_dictionary('C', dictionary, word))

                    if check_i:
                        if word not in ['УПЛ', 'НП', 'КП', 'БП', 'ЦФ', 'КФ', 'ЦВ', 'КВ', 'КС'] and not(is_m(word)) and not(is_aem(word)) and not(is_func(word)):
                            check('I', dictionary, word)
                            list_symb.append(return_from_dictionary('I', dictionary, word))
                        else:
                            # if word == 'НП':
                            #     list_symb[-2] = str(get_paramaters_start_function(dictionary, list_symb[-2]))
                            #     list_symb[-1] = str(get_paramaters_start_function(dictionary, list_symb[-1]))
                            list_symb.append(word)

                if is_simple_variable_type(word):
                    check('W', dictionary, word)
                    list_symb.append(return_from_dictionary('W', dictionary, word))
                    check_const = True

                if is_special_words(word):
                    check('W', dictionary, word)
                    list_symb.append(return_from_dictionary('W', dictionary, word))
                    check_const = True

                if is_operator(line[i]):
                    check('O', dictionary, line[i])
                    list_symb.append(return_from_dictionary('O', dictionary, line[i]))

                if is_separator(line[i]):
                    check('R', dictionary, line[i])
                    list_symb.append(return_from_dictionary('R', dictionary, line[i]))

                word = ''

            else:
                word+= line[i]
                if line[i] == "'" or line[i] == '"':
                    if check_str == False:
                        check_str = True
                    else:
                        check_str = False
                if word == 'КП' and i+1 == len(line):
                    list_symb.append(word)

        list_symb.append('\n')

    file_dict = open('file_dictionary.txt', 'w')
    for key in dictionary.keys():
        hat = output_table(key)
        file_dict.write(hat + '\n')
        for couple in dictionary[key].items():
            file_dict.write(couple[0] + '\t' + str(couple[1]) + '\n')
        file_dict.write('\n')

    file_dict.close()

    return list_symb, dictionary

# Возвращает переданный список, преобразованный в строку
def print_list(list_symb):
    str = ""
    for i in range(len(list_symb)):
        str += ' ' + list_symb[i]

    return str

# Записывает переданную строку в файл
def write_file(str):
    with open("file_out.txt", "w") as file:
        file.write(str)

# Возвращает содержимое файла
def read_file():
    with open("file_in.txt", 'r') as file:
        return list(map(str.strip, file.readlines()))


def main():
    list_symb, dictionary = scan(read_file())
    write_file(print_list(list_symb))


if __name__ == '__main__':
    main()