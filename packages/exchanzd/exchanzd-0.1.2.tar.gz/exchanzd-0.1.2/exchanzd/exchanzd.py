# todo for format_money
# case 1: format_money with only number argument provided.
# 1. add a symbol to number
# 2, add commas to number

def format_money(num: int = 0, sym='$'):
    num_list = list(str(num))
    if num_list[0] == '-':
        num_list.pop(0)
    num_list.reverse()
    counter = 0
    result = ''
    for n in num_list:
        counter += 1
        if counter % 3 == 0:
            result += n + ','
        else:
            result += n

    new_str = ''.join(list(reversed(result)))
    if new_str.startswith(','):
        new_str = new_str[1:]

    if num < 0:
        new_str = '-' + new_str

    return f'{sym}{new_str}'
