import first_lab as fl
import sys


# while, if, несколько функций;


out_str = list()
iterator = 0
current_symbol = ''
dictionary = dict()


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


def error():
    print('Ошибка!')
    exit(0)


def scan():
    global iterator, current_symbol
    current_symbol = out_str[iterator]
    iterator += 1


def program():
    if get_elem_dict() != 'void':
        error()

    scan()
    if get_elem_dict() != 'main':
        error()

    declare_params_main()

    scan()
    if get_elem_dict() != '{':
        error()

    scan()
    text()

    if get_elem_dict() != '}':
        error()


def text():
    while get_elem_dict() != '}':
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
    elif is_ident():
        scan()
        if get_elem_dict() == '=':
            scan()
            expression()
            if get_elem_dict() != ';':
                error()
            scan()
    else:
        error()


def declare():
    scan()
    if not is_ident():
        error()

    scan()
    while get_elem_dict() == ',':
        scan()
        if not is_ident():
            error()

        scan()

    if get_elem_dict() == '=':
        scan()
        expression()
    if get_elem_dict() == ';':
        scan()
    else:
        error()


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
            error()
        scan()
    else:
        argument()


def argument():
    check = False

    if not is_ident() and not is_const():
        error()

    if is_ident():
        check = True

    scan()
    if get_elem_dict() == '[' and check:
        scan()
        argument()
        if get_elem_dict() != ']':
            error()
        scan()


def declare_params_main():
    scan()
    if get_elem_dict() != '(':
        error()

    scan()
    if get_elem_dict() != 'char':
        error()

    scan()
    if get_elem_dict() != 'param':
        error()

    scan()
    if get_elem_dict() != ')':
        error()


def declare_args():
    scan()
    if get_elem_dict() != '(':
        error()

    scan()
    if get_elem_dict() == ')':
        scan()
        if get_elem_dict() != ';':
            error()
        scan()
        return

    expression()
    while get_elem_dict() == ',':
        scan()
        expression()

    if get_elem_dict() != ')':
        error()

    scan()
    if get_elem_dict() != ';':
        error()

    scan()


def is_for():
    scan()

    if get_elem_dict() != '(':
        error()

    declare()
    condition()
    if get_elem_dict() != ';':
        error()

    scan()
    step_loop()
    if get_elem_dict() != ')':
        error()

    scan()
    if get_elem_dict() != '{':
        error()

    scan()
    text()

    if get_elem_dict() != '}':
        error()
    scan()


def is_while():
    scan()

    if get_elem_dict() != '(':
        error()

    scan()
    condition()

    if get_elem_dict() != ')':
        error()

    scan()
    if get_elem_dict() != '{':
        error()

    scan()
    text()

    if get_elem_dict() != '}':
        error()

    scan()


def condition():
    expression()
    if get_elem_dict() not in ['<', '>', '==', '!=', '>=', '<=']:
        error()

    scan()
    expression()


def step_loop():
    if not is_ident():
        error()

    scan()
    if get_elem_dict() not in ['++', '--']:
        if get_elem_dict() != '=':
            error()
        scan()
        expression()
    elif get_elem_dict() in ['++', '--']:
        scan()
    else:
        error()


def declare_params_func():
    check_ident_end = True

    if get_elem_dict() != '(':
        error()

    scan()
    if not fl.is_simple_variable_type(get_elem_dict()) or not fl.is_composite_variable_type(get_elem_dict()):
        error()

    while get_elem_dict() == ',':
        pass


def main():
    global out_str, dictionary
    out_str, dictionary = fl.scan(fl.read_file())
    out_str = [el for el in out_str if el != '\n']
    print(out_str)
    try:
        scan()
        program()
    except:
        error()


if __name__ == '__main__':
    main()