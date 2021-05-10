import first_lab as fl
import sys


out_str = list()
iterator = 0
current_symbol = ''
dictionary = dict()
current_str = 1


def is_ident():
    return current_symbol[0] == 'I'


def is_const():
    return current_symbol[0] in ['N', 'C']


def get_elem_dict():
    key_word = current_symbol[0]
    value_word = int(current_symbol[1:])
    for key in dictionary[key_word]:
        if dictionary[key_word][key] == value_word:
            return key


def error(text):
    print('Ошибка!', text, 'Ошибка в строке:', current_str)
    exit(0)


def scan():
    global iterator, current_symbol
    current_symbol = out_str[iterator]
    iterator += 1


def program():
    global current_str
    if get_elem_dict() != 'void':
        error('Неправильная конструкция функции.')

    scan()
    if get_elem_dict() != 'main':
        error('Неправильное имя главной функции.')

    declare_params_main()

    scan()
    current_str += 1
    if get_elem_dict() != '{':
        error('Отсутствует символ начала описания функции.')

    scan()
    current_str += 1
    text()

    current_str += 1
    if get_elem_dict() != '}':
        error('Отсутствует символ окончания программы.')


def text():
    global current_str
    while get_elem_dict() != '}':
        current_str += 1
        operations()


def operations():
    if fl.is_simple_variable_type(get_elem_dict()) or fl.is_composite_variable_type(get_elem_dict()):
        declare()
    elif get_elem_dict() in ['printf', 'scanf', 'return', 'continue', 'getch', 'malloc', 'new']:
        declare_args()
    elif get_elem_dict() == 'for':
        is_for()
    elif get_elem_dict() == 'while':
        is_while()
    elif get_elem_dict() == 'if':
        is_if()
    elif is_ident():
        scan()
        if get_elem_dict() == '=':
            scan()
            expression()
            if get_elem_dict() != ';':
                error('Отсутствует символ окончания строки.')
            scan()
    else:
        error('Неизвестная конструкция.')


def declare():
    scan()
    if not is_ident():
        error('Неизвестный идентификатор при описании.')

    scan()
    while get_elem_dict() == ',':
        scan()
        if not is_ident():
            error('Неизвестный идентификатор при описании.')

        scan()

    if get_elem_dict() == '=':
        scan()
        expression()
    if get_elem_dict() == ';':
        scan()
    else:
        error('Неверная конструкция описания переменных.')


def expression():
    term()

    while get_elem_dict() in ['+', "-"] and get_elem_dict() != ';':
        scan()
        term()


def term():
    factor()

    while get_elem_dict() in ['*', "/"] and get_elem_dict() != ';':
        scan()
        factor()


def factor():
    if get_elem_dict() == '(':
        scan()
        expression()
        if get_elem_dict() != ')':
            error('Отсутствует закрывающая скобка.')
        scan()
    else:
        argument()


def argument():
    check = False

    if not is_ident() and not is_const():
        error('Неизвестный аргумент функции.')

    if is_ident():
        check = True

    scan()
    if get_elem_dict() == '[' and check:
        scan()
        argument()
        if get_elem_dict() != ']':
            error('Отсутствует закрывающая скобка при объявлении массива.')
        scan()


def declare_params_main():
    scan()
    if get_elem_dict() != '(':
        error('Пропущено объявление аргументов функции.')

    scan()
    if get_elem_dict() != 'char':
        error('Неверный тип аргумента у главной функции.')

    scan()
    if get_elem_dict() != 'param':
        error('Неизвестный аргумент для функции main.')

    scan()
    if get_elem_dict() != ')':
        error('Отсутствует закрывающая скобка.')


def declare_args():
    scan()
    if get_elem_dict() != '(':
        error('Отсутствует открывающая скобка.')

    scan()
    if get_elem_dict() == ')':
        scan()
        if get_elem_dict() != ';':
            error('Отсутствует символ окончания строки.')
        scan()
        return

    expression()
    while get_elem_dict() == ',':
        scan()
        expression()

    if get_elem_dict() != ')':
        error('Отсутствует закрывающая скобка.')

    scan()
    if get_elem_dict() != ';':
        error('Отсутствует символ окончания строки.')

    scan()


def is_for():
    global current_str
    scan()

    if get_elem_dict() != '(':
        error('Отсутствует открывающая скобка при объявлении оператора.')

    declare()
    condition()
    if get_elem_dict() != ';':
        error('Отсутствует разделитель при объявлении.')

    scan()
    step_loop()
    if get_elem_dict() != ')':
        error('Отсутствует закрывающая скобка.')

    scan()
    current_str += 1
    if get_elem_dict() != '{':
        error('Отсутсвует символ начала оператора.')

    scan()
    text()

    current_str += 1
    if get_elem_dict() != '}':
        error('Отсутствует символ окончания оператора.')
    scan()


def is_while():
    global current_str
    
    scan()
    if get_elem_dict() != '(':
        error('Отсутствует открывающая скобка при объявлении оператора.')

    scan()
    condition()

    if get_elem_dict() != ')':
        error('Отсутствует закрывающая скобка.')

    scan()
    if get_elem_dict() != '{':
        error('Отсутствует символ начала оператора.')

    scan()
    text()

    current_str += 1
    if get_elem_dict() != '}':
        error('Отсутствует символ окончания оператора.')

    scan()


def is_if():
    scan()

    if get_elem_dict() != '(':
        error('Отсутствует открывающая скобка при объявлении оператора.')

    scan()
    condition()

    if get_elem_dict() != ')':
        error('Отсутствует закрывающая скобка при объявлении оператора.')

    scan()
    if get_elem_dict() != '{':
        error('Отсутствует символ начала описания оператора.')

    scan()
    text()
    if get_elem_dict() != '}':
        error('Отсутствует символ окончания описания оператора.')

    scan()
    if get_elem_dict() == 'else':
        is_else()


def is_else():
    scan()
    if get_elem_dict() != '{':
        error('Отсутствует символ начала описания оператора.')

    scan()
    text()

    if get_elem_dict() != '}':
        error('Отсутствует символ окончания описания оператора.')

    scan()


def condition():
    expression()
    if get_elem_dict() not in ['<', '>', '==', '!=', '>=', '<=']:
        error('Неизвестный символ при описании условия.')

    scan()
    expression()


def step_loop():
    if not is_ident():
        error('Неизвестный идентификатор.')

    scan()
    if get_elem_dict() not in ['++', '--']:
        if get_elem_dict() != '=':
            error('Неверное объявление шага цикла.')
        scan()
        expression()
    elif get_elem_dict() in ['++', '--']:
        scan()
    else:
        error('Неверное объявление шага цикла.')


def declare_params_func():
    pass
    # if get_elem_dict() != '(':
    #     error('Отсутствует открывающая скобка ')
    #
    # scan()
    # if not fl.is_simple_variable_type(get_elem_dict()) or not fl.is_composite_variable_type(get_elem_dict()):
    #     error()
    #
    # while get_elem_dict() == ',':
    #     pass


def main():
    global out_str, dictionary
    out_str, dictionary = fl.scan(fl.read_file())
    out_str = [el for el in out_str if el != '\n']

    try:
        scan();
        program()
    except:
        pass


if __name__ == '__main__':
    main()