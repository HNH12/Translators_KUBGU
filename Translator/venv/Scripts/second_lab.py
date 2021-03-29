def is_separator(word):
    return (
        word in (';', '{', '}', '(', ')', ',', '[', ']')
    )

# True - если найдено совпадение word с элементом из списка односоставных типов
def is_simple_variable_type(word):
    return (
        word in ('short', 'char', 'int', 'signed', 'unsigned',
                 'long', 'float', 'double')
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
                 'static', 'printf', 'scanf', 'return', 'continue', 'void', 'getch', 'malloc')
    )

# True - если найдено совпадение word с элементом из списка операций
def is_operator(word):
    return (
        word in ('=', '!', '<', '>', '+', '-', '/', '%', '*', '$', '~')
    )

# Записывает переданную строку в файл
def write_file(str):
    with open("file_out.txt", "w") as file:
        file.write(str)

# Возвращает содержимое файла
def read_file():
    with open("file_in.txt", 'r') as file:
        return list(map(str.strip, file.readlines()))


def is_aem(str):
    if str.find('АЭМ') != -1:
        return True
    return False


def change_counter_aem(old_str):
    new_str = str(int(old_str[0]) + 1) + old_str[1:]
    return new_str


def is_func(str):
    if str.find('Ф') != -1:
        return True
    return False


def change_counter_func(old_str):
    new_str = str(int(old_str[0]) + 1) + old_str[1]
    return new_str


def priority(symb):
    if symb in ['(', '[', 'Ф', 'if'] or is_aem(symb):
        return 0
    elif symb in [')', ',', ']', 'else']:
        return 1
    elif symb in ['|']:
        return 2
    elif symb in ['&']:
        return 3
    elif symb in ['>', '<', '==']:
        return 5
    elif symb in ['+', '-']:
        return 6
    elif symb in ['*', '/']:
        return 7
    elif symb in ['**']:
        return 8
    else:
        return -1


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def is_if(str):
    if str.find('if') != -1:
        return True
    return False

def is_m(str):
    if str.find('М') != -1:
        return True
    return False

def counter_m(old_str):
    new_str = old_str[0] + str(int(old_str[1]) + 1)
    return new_str


def translate_to_opz(text):
    stack = list()
    out_str = ''
    for line in text:
        word = ''
        check_str = False
        check_func = False
        check_if = False
        check_else = False
        check_end_if = False

        for i in range(len(line)):
            if not(check_str) and (line[i] == ' ' or is_separator(line[i]) or is_operator(line[i])) and len(line[i]) != 0:
                if priority(word) == -1 and not(is_separator(word)):
                    out_str += word + ' '

                # Старт перевода в условный оператор
                if word == 'if':
                    check_if = True
                    stack.append(word)
                    stack.append('(')

                # Старт перевода в опз записи массива (приоритет для того, что отследить, что это идентификатор)
                elif line[i] == '[' and priority(word) == -1 and not(is_number(word)) and word != '' and not(is_special_words(word)):
                    stack.append('2АЭМ')

                # Старт перевода в опз записи функции (опять же приоритет)
                elif line[i] == '(' and priority(word) == -1 and not(is_number(word)) and word != '' and not(is_special_words(word)):
                    stack.append('1Ф')
                    check_func = True

                # По шагу из методички. Если запятая, то выносим все до ключевого слова
                elif line[i] == ',':
                    while not(is_aem(stack[-1])) and not(is_func(stack[-1]) and not(is_if(stack[-1]))):
                        last_elem = stack.pop()
                        out_str += last_elem + ' '
                    if is_aem(stack[-1]):
                        stack[-1] = change_counter_aem(stack[-1])
                    elif is_func(stack[-1]):
                        stack[-1] = change_counter_func(stack[-1])

                # Если закрывается запись массива, то просто выводим в строку АЭМ
                elif line[i] == ']':
                    last_elem = stack.pop()
                    out_str += last_elem + ' '

                # То же самое, но с Ф (вывести все до Ф)
                elif line[i] == ')' and check_func:
                    while not(is_func(stack[-1])):
                        out_str += stack.pop() + ' '
                    last_elem = stack.pop()
                    out_str += change_counter_func(last_elem) + ' '
                    check_func = False

                # Обрабатывает начало тела if
                elif line[i] == '{' and check_if:
                    while not(is_if(stack[-1])):
                        out_str += stack.pop() + ' '
                    check_if = False
                    check_end_if = True
                    stack.append('М1')
                    out_str += stack[-1] + ' УПЛ '

                # Обрабатывает else
                elif word == 'else':
                    while not(is_m(stack[-1])):
                        out_str += stack.pop() + ' '
                    out_str += counter_m(stack[-1]) + ' БП ' + stack[-1] + ':'
                    stack[-1] = counter_m(stack[-1])
                    check_else = True

                # Если else, то такое завершение
                elif line[i] == '}' and check_else:

                    while not(is_m(stack[-1])):
                        out_str += stack.pop() + ' '
                    out_str += stack.pop() + ': '
                    check_else = False
                    check_end_if = False
                    stack.pop()

                # Если без else, то другое завершение
                elif line[i] == '}' and check_end_if:
                    while not(is_m(stack[-1])):
                        out_str += stack.pop() + ' '
                    out_str += stack.pop() + ': '
                    stack.pop()

                elif len(stack) == 0 and priority(line[i]) > -1 and line[i] != '':
                    stack.append(line[i])

                elif line[i] == '(':
                    stack.append(line[i])

                elif line[i] == ')':
                    while stack[-1] != '(':
                        out_str += stack.pop() + ' '
                    stack.pop()

                # Чтобы специальные обозначения не смущали операции при заносе в стек
                elif ((priority(stack[-1]) <= priority(line[i])) and priority(line[i]) > -1 and line[i] != '') or is_aem(stack[-1]) or is_func(stack[-1]) or is_if(stack[-1]):
                    stack.append(line[i])

                # Чтобы специальные обозначения не смущали операции при заносе в стек
                elif priority(stack[-1]) > priority(line[i]) and priority(line[i]) > -1 and line[i] != '':
                    while len(stack) > 0 and priority(stack[-1]) > priority(line[i]) and not(is_aem(stack[-1])) and not(is_func(stack[-1])) and not(is_if(stack[-1])):
                        last_elem = stack.pop()
                        out_str += last_elem + ' '
                    stack.append(line[i])

                word = ''

            else:
                word += line[i]
                if line[i] == "'" or line[i] == '"':
                    if check_str == False:
                        check_str = True
                    else:
                        check_str = False

        while len(stack) > 0:
            last_elem = stack.pop()
            out_str += last_elem + ' '

    return out_str


def main():
    result = (translate_to_opz(['(a+b[i+20,j])*c+d;', 'y-f(x,z,y+2);','if(a>b) { x+1; }']))
    result = ' '.join(map(str.strip, result.split()))
    print(result)


if __name__ == '__main__':
    main()