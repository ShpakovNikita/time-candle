from tokenize import tokenize
from io import BytesIO
from collections import namedtuple
from time_candle.storage.task_adapter import TaskFilter
import time_candle.exceptions.show_me_exceptions as sm_e
import time_candle.model.time_formatter as formatter


_token_format = namedtuple('token_format',
                           ['type_code', 'value', 'begin', 'end'])


def _get_filter_from_list_title(lst, fil):
    for arg in lst:
        fil.title_substring(arg, TaskFilter.OP_OR)

    return fil


def int_or_none(val):
    try:
        return None if val.upper() == 'NONE' else int(val)
    except ValueError:
        raise sm_e.InvalidExpressionError(
            sm_e.ShowMeMessages.UNEXPECTED_LITERAL_TYPE)


OPERATORS = {'OR': (1, lambda x, y: x | y), 'AND': (2, lambda x, y: x & y)}
SIMPLE_COMMANDS = {
    'projects': lambda lst, fil: fil.project(list(map(int_or_none, lst))),
    'receivers': lambda lst, fil: fil.receiver(list(map(int_or_none, lst))),
    'creators': lambda lst, fil: fil.creator(list(map(int_or_none, lst))),
    'tids': lambda lst, fil: fil.tid(list(map(int_or_none, lst))),
    'parents': lambda lst, fil: fil.parent(list(map(int_or_none, lst))),
    'titles': lambda lst, fil: _get_filter_from_list_title(lst, fil)
}

# it will return only method
TIME_COMMANDS = {
    'deadline_time': lambda fil: fil.deadline_time,
    'creation_time': lambda fil: fil.creation_time
}

COMPARE_OPERATORS = {
    '>': TaskFilter.OP_GREATER,
    '>=': TaskFilter.OP_GREATER_OR_EQUALS,
    '==': TaskFilter.OP_EQUALS,
    '<=': TaskFilter.OP_LESS_OR_EQUALS,
    '<': TaskFilter.OP_LESS,
    '!=': TaskFilter.OP_NOT_EQUALS
}


def shunting_yard(parsed_formula):
    stack = []
    for token in parsed_formula:
        if token in OPERATORS:
            while stack and stack[-1] != "(" and \
                    OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                yield stack.pop()
            stack.append(token)
        elif token == ")":
            while stack:
                x = stack.pop()
                if x == "(":
                    break
                yield x
        elif token == "(":
            stack.append(token)
        else:
            yield token
    while stack:
        yield stack.pop()


def calc(polish):
    stack = []
    for token in polish:
        if token in OPERATORS:
            try:
                y, x = stack.pop(), stack.pop()
            except IndexError:
                raise sm_e.InvalidExpressionError(sm_e.ShowMeMessages)
            stack.append(OPERATORS[token][1](x, y))
        else:
            stack.append(token)
    return stack[0]


def parse_string(data):
    """
    This function parses passed data in the following type to the commands and
    filters
    :param data: String of filters to show
    :return: None
    """
    # (projects: 1 3 4 OR projects: 1 3 6) AND tids: 2 3 1
    result = _get_tokens(data)
    result = [(lambda s: eval(s) if s.startswith(('"', "'")) else s)
              (token) for token in result]

    fil = calc(shunting_yard(_bond_expressions(result)))
    return fil


def _get_tokens(data):
    # This function returns list of tokens in the token_format format
    result = []

    # tokenize the string
    g = tokenize(BytesIO(data.encode('utf-8')).readline)
    for toknum, tokval, tup_begin, tup_end, _ in g:

        # if we on the first line then add tokens
        if tup_end[0] == 1:
            result.append(_token_format(type_code=toknum,
                                        value=tokval,
                                        begin=tup_begin[1],
                                        end=tup_end[1]))

    return [token.value for token in result]


def _bond_expressions(tokens):
    expr = tokens
    # expr = [f.value for f in tokens]
    i = 0
    filter_sequence = []

    def next_character_is_execute(x):
        return x < len(expr) - 1 and expr[x + 1] == ':'

    # this function extends list by adding executable operands and returning
    # it's length
    def get_list_before_next_action(action_list):
        current_len = 0
        while True:
            if i + current_len >= len(expr):
                break
            elif expr[i + current_len] in SIMPLE_COMMANDS \
                    or expr[i + current_len] in OPERATORS \
                    or expr[i + current_len] in '()':
                break

            action_list.append(expr[i + current_len])
            current_len += 1

        if current_len == 0:
            raise sm_e. \
                FewElementsError(sm_e.ShowMeMessages.NO_ELEMENTS_FOR_FILTER)

        return current_len

    # iterate all over the statements
    while i < len(expr):
        # if we found command then we should generate filter for it
        if expr[i] in SIMPLE_COMMANDS and next_character_is_execute(i):
            fil, lst, command = TaskFilter(), [], expr[i]
            # skip two words due to we are already read them
            i += 2
            sub_i = get_list_before_next_action(lst)

            SIMPLE_COMMANDS[command](lst, fil)
            filter_sequence.append(fil)
            i += sub_i

        # special commands needs an another filters
        elif expr[i] in TIME_COMMANDS and next_character_is_execute(i):
            fil, lst, command = TaskFilter(), [], expr[i]
            i += 2
            sub_i = get_list_before_next_action(lst)

            # running through our filters and searching for matching. Else we
            # are just raising error, because no templates were found
            success_flag = False
            for filter_func in FILTERS_LIST:
                try:
                    success_flag = filter_func(lst, fil, command)
                    if success_flag:
                        break

                except IndexError:
                    pass

            if not success_flag:
                raise sm_e.InvalidExpressionError(
                    sm_e.ShowMeMessages.INVALID_TEMPLATE_USAGE)

            filter_sequence.append(fil)
            i += sub_i

        # just for brackets
        elif expr[i].upper() in OPERATORS or expr[i] in '(){}[]' and expr[i]:
            filter_sequence.append(expr[i])
            i += 1

        elif not expr[i]:
            if len(expr) == 1 and expr[0] == '':
                filter_sequence.append(TaskFilter())

            break
        else:
            raise sm_e. \
                InvalidExpressionError(sm_e.ShowMeMessages.
                                       UNEXPECTED_SYMBOL_FOUND)

    return filter_sequence


################################################################################
# SPECIAL FILTER FUNCTIONS                                                     #
################################################################################
def _get_time_range_filter(lst, fil, command):
    if len(lst) == 4 and lst[1] == '.' and lst[2] == '.':
        lower_bound = formatter.get_milliseconds(lst[0])
        upper_bound = formatter.get_milliseconds(lst[3])

        TIME_COMMANDS[command](fil)(lower_bound, COMPARE_OPERATORS['>='])
        TIME_COMMANDS[command](fil)(upper_bound, COMPARE_OPERATORS['<='])

        return True

    return False


def _get_time_compare_filter(lst, fil, command):
    if len(lst) == 2 and lst[0] in COMPARE_OPERATORS:
        bound = formatter.get_milliseconds(lst[1])
        TIME_COMMANDS[command](fil)(bound, COMPARE_OPERATORS[lst[0]])

        return True

    return False


FILTERS_LIST = [_get_time_compare_filter, _get_time_range_filter]
