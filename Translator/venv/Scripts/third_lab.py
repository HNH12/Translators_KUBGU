import second_lab as sl
import first_lab as fl


def is_w(word):
    return word[0] == 'W'


def is_type(word, dictionary):
    key_word = word[0]
    value_word = int(word[1:])
    for key in dictionary[key_word]:
        if dictionary[key_word][key] == value_word:
            if fl.is_simple_variable_type(key) or fl.is_composite_variable_type(key):
                return True
    return False


def get_elem_dict(word, dictionary):
    key_word = word[0]
    if key_word not in ['К', 'Ц', 'Н'] and not(fl.is_number(key_word)):
        value_word = int(word[1:])
        for key in dictionary[key_word]:
            if dictionary[key_word][key] == value_word:
                return key
    else:
        return word



def get_O(word,dictionary):
    pass


def is_O(word):
    return word[0] == 'O'


def is_func(word):
    return word[1] == 'Ф'


def split_func(func):
    index = func.index('(')
    last_index = func.index(')')
    return (func[0:index] + func[last_index+1:], func[index+1:last_index])


def get_params(func, params):
    index = func.index('(')
    last_index = func.index(')')

    return func[0:index+1] + params + func[last_index]


def get_variable_perl(text, dictionary, dictionary_r):
    sublist = text.split('\n')
    for i in range(len(sublist)):
        words = sublist[i].split()
        if words:
            if words[0] == 'sub':
                name_func, params = split_func(words[1])
                new_str = get_params(sublist[i+2].split()[0], params)
                new_arr = sublist[i+2].split()
                new_arr[0] = new_str
                sublist[i] = 'sub ' + name_func
                sublist[i+2] = ' '.join(new_arr)

            elif words[-1] == '$=':
                new_str = ""
                if len(words) > 2:
                    new_str += "$" + words[0] + ' ' + words[-1][1] + " " + words[1]
                else:
                    new_str += "my @" + get_elem_dict(words[0], dictionary)
                sublist[i] = new_str

            elif is_O(words[-1]):
                new_str = ""
                new_str += words[0] + " " + words[-1] + " " + words[1]
                sublist[i] = new_str

    return sublist


def transalate_R(out_str, dictionary, dictionary_R):
    new_str = list()
    for l in out_str:
        while l.find('R') != -1:
            replace_symb = l[l.find('R')] + l[l.find('R') + 1]
            l = l.replace(replace_symb, dictionary_R[replace_symb])
        while l.find('I') != -1:
            replace_symb = l[l.find('I')] + l[l.find('I') + 1]
            l = l.replace(replace_symb, get_elem_dict(replace_symb, dictionary))
        while l.find('O') != -1:
            replace_symb = l[l.find('O')] + l[l.find('O') + 1]
            l = l.replace(replace_symb, get_elem_dict(replace_symb, dictionary))
        while l.find('N') != -1:
            replace_symb = l[l.find('N')] + l[l.find('N') + 1]
            l = l.replace(replace_symb, get_elem_dict(replace_symb, dictionary))
        if l != '{' and l != '}' and l.find('sub') == -1 and l.find('while') == -1 and l.find('if') == -1 \
                and l.find('for') == -1 and l!='' and l.find('else') == -1:
            l += ';'
        new_str.append(l)

    return new_str


def translate_to_file_perl(out_str):
    with open('perl_file_out.txt','w') as file:
        file.write('\n'.join(out_str))


def translator(text, dictionary):
    count_R = 0
    new_dict = dict()
    stack = list()
    count_func = 0
    out_str = ""
    for line in text:
        size = len(line.split(' '))
        line = line.split(' ')
        for i in range(size):

            # print('ITER NUMB: ', i, '\n', out_str, '\n', 'СТЕК:', stack, '\n\n'

            if line[i] == '0АЭМ':
                if len(stack) > 0 and 'new' == get_elem_dict(stack[-2], dictionary):
                    stack.pop()
                    stack.pop()
                    stack.append('()')
                continue

            if line[i][-1] == 'М':
                const_N = line[i][0]
                new_arr = list()
                for _ in range(int(get_elem_dict(const_N, dictionary))):
                    new_arr.append(stack.pop())
                new_str_arr = "$" + new_arr[-1] + '['
                for _ in range(2, len(new_arr)+1):
                    new_str_arr += new_arr[-_]
                    if _ != len(new_arr):
                        new_str_arr += ','
                new_str_arr += ']'
                stack.append(new_str_arr)
                continue

            if line[i] == 'НП':
                stack.pop()
                stack.pop()

                out_str += 'sub ' + str(stack.pop()) + '\n{\nmy('
                out_str += ') = @_'
                count_func += 1
                continue

            if line[i] == 'КС':
                if count_func > 0:
                    if len(stack) > 0:
                        help_list = list()
                        while len(stack) > 0:
                            help_list.append(str(stack.pop()))
                        for _ in range(1, len(help_list)+1):
                            out_str += help_list[-_] + ' '
                        out_str += '\n'
                    else:
                        out_str += '\n'
                continue

            if line[i] == 'КП':
                count_func -= 1
                out_str += '}\n\n'
                continue

            if line[i] == 'УПЛ':
                out_str += '\nif('
                stack.pop()
                if_list = list()
                while len(stack) > 0:
                    if_list.append(str(stack.pop()))
                for _ in range(1, len(if_list)+1):
                    out_str += if_list[-_] + ' '
                out_str += ')\n{'
                continue

            if line[i][0] == 'М' and line[i][-1] == ':':
                if len(stack) > 0:
                    while len(stack) > 0:
                        stack.pop()
                    out_str += '}\nelse {\n'
                else:
                    out_str += '}'
                continue

            if line[i] == 'ЦФ':
                new_for = [stack.pop(), stack.pop(), stack.pop(),stack.pop(),stack.pop(),stack.pop(),stack.pop()]
                out_str += 'for( ' + str(new_for[-1]) + ' ' + str(new_for[-3]) + ' ' + str(new_for[-2]) + ' ; ' + \
                           str(new_for[-4]) + ' ; ' + str(new_for[-5]) + ' ' + str(new_for[-7]) + ' ' + str(new_for[-6]) + ' )\n{'
                continue
            if line[i] == 'КФ':
                out_str += '}\n'
                continue
            if line[i] == 'ЦВ':
                out_str += ' while(' + str(stack.pop()) + ')\n{\n'
                continue
            if line[i] == 'КВ':
                out_str += '}\n'
                continue

            if is_func(line[i]):
                const_N = line[i][0:len(line[i])-1]
                param_func = list()
                for _ in range(int(const_N)):
                    new_elem = stack.pop()
                    if new_elem[0] != '$':
                        if(new_elem[0] == 'R'):
                            param_func.append(new_elem)
                        else:
                            param_func.append(get_elem_dict(new_elem, dictionary))
                    else:
                        param_func.append(new_elem)
                new_func = ""
                if param_func[-1][0] == '$':
                    new_func += param_func[-1][1:]
                else:
                    new_func += param_func[-1]
                new_func += '('
                for _ in range(2, len(param_func)+1):
                    new_func += param_func[-_]
                    if _ != len(param_func):
                        new_func += ','
                new_func += ')'
                stack.append(new_func)
                continue

            if is_O(line[i]):
                if get_elem_dict(line[i], dictionary) == '&' and not(is_O(stack[-1])):
                    stack.append(line[i])
                    continue
                if get_elem_dict(line[i], dictionary) == '=' and not(is_O(stack[-1])):
                    stack.append(line[i])
                    continue
                second_el = stack.pop()
                first_el = stack.pop()
                current_O = get_elem_dict(line[i], dictionary)
                if current_O in ['<', '>', '+', '-', '/', '%', '*', '&', '|']:
                    new_R = first_el + ' ' + current_O + ' ' + second_el
                    current_R = 'R' + str(count_R)
                    new_dict[current_R] = new_R
                    stack.append(current_R)
                    count_R += 1
                else:
                    out_str += ' ' + first_el + ' ' + current_O + ' ' + second_el

            elif is_w(line[i]) and is_type(line[i], dictionary):
                const_N = stack.pop()
                new_temp = ""
                for j in range(int(get_elem_dict(const_N, dictionary))):
                    last_el = stack.pop()
                    if last_el[0] == 'R':
                        new_temp += '$' + last_el
                    else:
                        if last_el[0] == '(':
                            break
                        else:
                            new_temp += '$' + str(get_elem_dict(last_el, dictionary))
                    if j < int(get_elem_dict(const_N, dictionary)) - 1:
                        new_temp += ', '
                if new_temp != "":
                    stack.append(new_temp)

            else:
                stack.append(line[i])

    translate_to_file_perl(transalate_R(get_variable_perl(out_str, dictionary, new_dict), dictionary, new_dict))


def read_file():
    with open("file_out.txt", 'r') as file:
        return list(map(str.strip, file.readlines()))


def main():
    dictionary = sl.main()
    print(dictionary)
    translator(read_file(), dictionary)


if __name__ == '__main__':
    main()