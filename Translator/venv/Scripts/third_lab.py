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

            # print('ITER NUMB: ', i, '\n', out_str, '\n', 'СТЕК:', stack, '\n\n')

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
                        while len(stack) > 0:
                            out_str += str(stack.pop())
                        out_str += '\n'
                    else:
                        out_str += '\n'
                continue

            if line[i] == 'КП':
                count_func -= 1
                out_str += '}'
                continue

            if line[i] == 'УПЛ':
                out_str += 'if('
                stack.pop()
                if_list = list()
                while len(stack) > 0:
                    if_list.append(str(stack.pop()))
                for _ in range(1, len(if_list)+1):
                    out_str += if_list[-_]
                out_str += ')\n{'
                continue

            if line[i][0] == 'М' and line[i][-1] == ':':
                if len(stack) > 0:
                    while len(stack) > 0:
                        stack.pop()
                    out_str += '}\nelse{\n'
                else:
                    out_str += '}'
                continue


            if line[i] == 'ЦФ':
                new_for = [stack.pop(), stack.pop(), stack.pop()]
                out_str += 'for(' + str(new_for[-1]) + ';' + str(new_for[-2]) + ';' + str(new_for[-3]) + ')\n{\n'
                continue
            if line[i] == 'КФ':
                out_str += '}\n'
                continue
            if line[i] == 'ЦВ':
                out_str += 'while(' + str(stack.pop()) + ')\n{\n'
                continue
            if line[i] == 'КВ':
                out_str += '}\n'
                continue

            if is_func(line[i]):
                const_N = line[i][0:len(line[i])-1]
                param_func = list()
                print('zc', stack, const_N)
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
                print('zz',param_func)
                if param_func[-1][0] == '$':
                    new_func += param_func[-1][1:]
                else:
                    new_func += param_func[-1]
                new_func += '('
                for _ in range(2, len(param_func)+1):
                    new_func += param_func[-_]
                    if _ != len(param_func):
                        new_func += ', '
                new_func += ')'
                print(new_func)
                stack.append(new_func)
                continue

            if is_O(line[i]):
                print('hh', stack, get_elem_dict(line[i], dictionary))
                if get_elem_dict(line[i], dictionary) == '&' and get_elem_dict(stack[-1],dictionary) != '&':
                    stack.append(line[i])
                    continue
                second_el = stack.pop()
                first_el = stack.pop()
                current_O = get_elem_dict(line[i], dictionary)
                if current_O in ['<', '>', '+', '-', '/', '%', '*', '=', '&', '|']:
                    new_R = get_elem_dict(first_el, dictionary) + ' ' + current_O + ' ' + second_el
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
                        new_temp += '$' + str(get_elem_dict(last_el, dictionary))
                    if j < int(get_elem_dict(const_N, dictionary)) - 1:
                        new_temp += ', '
                    print(new_temp, end=' ')
                stack.append(new_temp)
                print('tut', stack, line[i], end='\n')
            else:
                stack.append(line[i])
    print(out_str, new_dict)




def read_file():
    with open("file_out.txt", 'r') as file:
        return list(map(str.strip, file.readlines()))


def main():
    dictionary = sl.main()
    print(dictionary)
    translator(read_file(), dictionary)



if __name__ == '__main__':
    main()