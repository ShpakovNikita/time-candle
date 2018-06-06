from tokenize import tokenize
from io import BytesIO
from collections import namedtuple
from time_candle.storage.task_adapter import TaskFilter
import time_candle.exceptions.show_me_exceptions as sm_e


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
COMMANDS = {
    'projects': lambda lst, fil: fil.project(list(map(int_or_none, lst))),
    'receivers': lambda lst, fil: fil.receiver(list(map(int_or_none, lst))),
    'creators': lambda lst, fil: fil.creator(list(map(int_or_none, lst))),
    'tids': lambda lst, fil: fil.tid(list(map(int_or_none, lst))),
    'titles': lambda lst, fil: _get_filter_from_list_title(lst, fil)}

COMPARE_OPERATORS = {}


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
    # data = ""
    result = _get_tokens(data)

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
    # iterate all over the statements
    while i < len(expr):
        # if we found command then we should generate filter for it
        if expr[i] in COMMANDS and i < len(expr) - 1 and expr[i + 1] == ':':
            fil, lst, command = TaskFilter(), [], expr[i]
            i += 2
            sub_i = 0
            while True:
                if i + sub_i >= len(expr):
                    break
                elif expr[i + sub_i] in COMMANDS \
                        or expr[i + sub_i] in OPERATORS \
                        or expr[i + sub_i] in '()':
                    break

                lst.append(expr[i + sub_i])
                sub_i += 1

            if sub_i == 0:
                raise sm_e. \
                    FewElementsError(sm_e.ShowMeMessages.NO_ELEMENTS_FOR_FILTER)

            COMMANDS[command](lst, fil)
            filter_sequence.append(fil)
            i += sub_i
        elif expr[i] in OPERATORS or expr[i] in '()' and expr[i]:
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
