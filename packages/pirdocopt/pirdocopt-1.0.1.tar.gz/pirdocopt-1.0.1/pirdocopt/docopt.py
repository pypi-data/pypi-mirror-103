"""
 Docopt is for making beautiful command line program for python.
"""
import math
import re
import sys
import warnings
import docopt_util


def docopt(doc, version=None, help_message=True, argv=None):
    """ Main function for docopt program

    Args:
        doc: docstring that pass from the user program

        argv: programmer can pre-pass some parameters into docopt and
        those parameters is treat as default existing arguments

        help_message: user can specify whether they want docopt to display
        the help message whenever user execute the program

        version: programmers can specify the version of
        the project and display to user
    Returns:
        total_dic: returns the complete dictionary from parameters passed in

    >>>  doc0 = "Perfect" \
    >>>
    >>>         "Usage:" \
    >>>           "naval_fate.py ship new <name>..." \
    >>>           "naval_fate.py ship <name> move <x> <y> [--speed=<kn>]" \
    >>>
    >>>         "Options:" \
    >>>           '-h --help --helping --haha -hhh Show this screen.' \
    >>>           '-o FILE --output=<value>  Speed in knots [default: ./test.txt].' \
    >>>           '--speed=<kn> -s KN  Speed in knots [default: 10].' \
    >>>
    >>>  docopt(doc=doc0, version="test 2.0", help_message=False,
    >>>                    argv=['ship', 'Titanic', 'move', 10, 90, '--speed=70'])
    {'ship': True, 'new': False, '<name>...': False, 'name': 'Titanic', 'move': True,
    'x': 10, 'y': 90, '--helping': False, '--output': './test.txt', '--speed': 70}
    """

    usages, options_array = processing_string(
        doc, help_message, version)
    args = sys.argv[1:]
    if len(args) == 0 and argv is not None:
        args = argv

    if 'Usage:' in usages[0]:
        tmp = usages[0].split()
        if len(tmp) == 1:
            usages.pop(0)
        else:
            usages[0] = ' '.join(tmp[1:])

    output_dic, tree_heads = get_heads_and_dict(usages, options_array)
    output_dic = match_user_input(tree_heads, output_dic, args)
    total_dic, output_string = print_output_dictionary(output_dic)
    print(output_string)
    return total_dic


def processing_string(doc, help_message, version):
    """
    Args:
        doc: docstring pass from the main function.
        help_message: to tell docopt whether user want to display help message when
                      the program executes.
        version: the version string pass from main function.
        version: programmers can specify the version of the project and display to user.
    Returns:
        usage.split("\n"): returns the array of usage patterns.
        options.split("\n"): returns the array of options from docstring.
    >>> doc1 = 'Perfect' \
    >>>
    >>>        'Usage:' \
    >>>          'naval_fate.py ship new <name>...' \
    >>>
    >>>        'Options:' \
    >>>           '-h --help --helping Show this screen.' \
    >>>           '--sorted  Show sorted.'
    >>>
    >>> processing_string(doc=doc1, help_message=False, version="test 2.0")
    ['Usage:', '  naval_fate.py ship new <name>...'], \
    ['Options:', '  -h --help --helping Show this screen.', '  --sorted  Show sorted.']
    """

    if doc is None:
        warnings.warn('No docstring found')
        return None
    _, usage, options, display_help = get_usage_and_options(doc, version)
    check_warnings(usage, options)
    if help_message:
        print(display_help)
    return usage.split("\n"), options.split("\n")


# Helper function for getting usage, options and name strings from doc
def get_usage_and_options(doc, version):
    """
    Args:
        doc: docstring that passed from main function.
        version: the version string pass from main function.
    Returns:
        name: returns the strings of name of program.
        usage: returns the strings of usage patterns.
        options: returns the strings of options that received from docstring
    >>> doc1 = 'Perfect' \
    >>>
    >>>        'Usage:' \
    >>>          'naval_fate.py ship new <name>...' \
    >>>
    >>>        'Options:' \
    >>>           '-h --help --helping Show this screen.' \
    >>>           '--sorted  Show sorted.'
    >>>
    >>> get_usage_and_options(doc1)
    "Perfect",
    "Usage: \
    naval_fate.py ship new <name>...", \
    "Options: \
    -h --help --helping Show this screen. \
    --sorted  Show sorted."
    """
    usage = ""
    options = ""
    partition_string = doc.strip().split('\n\n')
    name = partition_string[0].strip()
    partition_string.pop(0)

    if name is not None and not isinstance(usage, str) or \
            version is not None and not isinstance(version, str):
        raise docopt_util.DocoptExit("Argument type error occur")

    if "Usage:" in name:
        usage = name
        name = ""
    else:
        for element in partition_string:
            if 'Usage:' in element.strip():
                usage = element
                partition_string.remove(element)

    if version is not None and len(name) > 0:
        display_help = name + "\n\n" + "Version:\n" + version + "\n\n" + usage + "\n\n" + \
                       "\n\n".join(partition_string) + "\n\n"
    elif version is not None:
        display_help = "Version:\n  " + version + "\n\n" + usage + "\n\n" + "\n\n".join(
            partition_string) + "\n\n"
    elif len(name) > 0:
        display_help = name + "\n\n" + usage + "\n\n" + "\n\n".join(
            partition_string) + "\n\n"
    else:
        display_help = usage + "\n\n" + "\n\n".join(partition_string) + '\n\n'

    for element in partition_string:
        if element.strip()[:1] == '-' or 'Options:' in element.strip():
            options = element
            partition_string.remove(element)
    return name, usage, options, display_help


# Will display warning to the user program when missing parts
def check_warnings(usage, options):
    """ Function for testing whether the docstring contains a usage part and a options part.
    Args:
        usage: a string the retrieve from the docstring.
        options: a string that retrieve from the docstring.
    Returns:
        returns 1 if no usage pattern found, returns 2 if no options found,
        and returns 0 if everything is ok in docstring
    Raises:
        Warnings: If no usages or options contained in the docstring.
    >>> check_warnings(usage="Usages: ...", options="")
    0
    >>> check_warnings(usage="", options="Options: ...")
    1
    >>> check_warnings(usage="Usages: ...", options="")
    2
    """
    if len(usage) == 0:
        warnings.warn('No usage indicated from docstring')
        return 1
    if len(options) == 0:
        warnings.warn('No options indicated from docstring')
        return 2
    return 0


# Main function for building output strings to user
def print_output_dictionary(usage_dic):
    """
    Args:
        usage_dic: the original usage dictionary from main function.
    Returns:
        dictionary_total: the final dictionary object that built from usage pattern and options.
        return the formatted json like dictionary string to user.
    >>> input1 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha'}
    >>> u_dic = {'usage1': 'x', 'usage2': 'y'}
    >>> dic_total, res = print_output_dictionary(usage_dic=u_dic, options_dic=input1)
    >>> assert dic_total == {**usage_dic, **dic_total}
    {'usage1': 'x'
     'usage2': 'y'
     '1': True
     '2': 'haha'
     '3': False
     '4': True
     '5': 'haha'}
    """
    dictionary_total = dict.copy(usage_dic)
    dic_list = list(dictionary_total)
    length = len(dictionary_total)
    if length > 24:
        rows = math.ceil(length / 3)
    else:
        rows = 8
    return dictionary_total, output_formatter(rows, length, dic_list, dictionary_total)


def match_user_input(tree_heads, usage_dic, args):
    """
    matches user input against usage patterns
    Args:
        tree_heads: the head nodes of the matching token tree
        usage_dic: the dictionary for holding all the keywords
        args: list of incoming tokens
    Returns:
        True if a match is found else False
    """
    index = 0
    for head in tree_heads:
        head_dict = dict()
        old_index = index
        is_match, index, dic_entry = head.match(args, index)
        if not is_match:
            index = old_index
            continue
        head_dict.update(dic_entry)
        children_match = get_child_match(head.children, args, index, head_dict)
        if children_match:
            usage_dic.update(head_dict)
    return usage_dic


def get_child_match(children, args, index, head_dict):
    """
    matching function for children nodes
    Args:
        children: the list of children nodes for a head node
        args: list of incoming tokens
        index: position in args list where comparison continues
        head_dict: the dictionary that is going to be updated
    Returns:
        True if a match is found else False
    """
    children_match = False
    if not children:
        children_match = True
    for child in children:
        child_dict = dict()
        old_index = index
        is_match, index, dic_entry = child.match(args, index)
        if not is_match:
            index = old_index
            continue
        child_dict.update(dic_entry)
        post_match = get_post_match(child, args, index, child_dict)
        if post_match:
            children_match = True
            head_dict.update(child_dict)
            break
        index = old_index
    return children_match


def get_post_match(child, args, index, child_dict):
    """
    matching function for post nodes
    Args:
        child: the matched child from which we check post tokens.
        args: list of incoming tokens.
        index: position in args list where comparison continues.
        child_dict: the dictionary that is going to be updated.
    Returns:
        True if a match is found else False.
    """
    post = child.post
    post_match = True
    while post:
        is_match, index, dic_entry = post.match(args, index)
        if not is_match:
            post_match = False
            break
        child_dict.update(dic_entry)
        post = post.post
    return post_match


def get_heads_and_dict(usages, options):
    """
    Args:
        usages: array of usage pattern from docstring.
        options: array of option keywords from docstring.
    Returns:
        usage pattern, keyword dictionary, and array of token of
        the first layer of the tree structure.
    """
    new_usages = []
    usage_dic = {}
    tree_heads = []
    options_pat = check_option_lines(options)
    for pattern in usages:
        pattern = re.sub(r'([\[\]()|]|\.\.\.)', r' \1 ', pattern).split()
        pattern.pop(0)
        pattern = identify_tokens(pattern, options_pat)
        create_opt_and_req(pattern)
        create_mutex(pattern)
        create_repeating(pattern)
        for index, token in enumerate(pattern):
            if isinstance(token.post, docopt_util.SpecialToken) and index < len(pattern) - 1:
                print('dsadasddadasd')
                token.post = pattern[index + 1]
        new_usages.append(pattern)
        usage_dic.update(dict_populate_loop(pattern))
        tree_heads = build_tree_heads(pattern, tree_heads)

    for pattern in new_usages:
        for index, token in enumerate(pattern):
            token.post = pattern[index + 1] if index + \
                                               1 < len(pattern) else None
    return usage_dic, tree_heads


def is_num(arg):
    """
    Args:
        arg: input object that going to check if it is a number.
    Returns:
        true is input is number, else return false.
    """
    try:
        float(arg)
        return True
    except ValueError:
        return False


def set_children(pattern):
    """
    Args:
        pattern: array of tokens that represents the tokens.
    """
    for token in pattern:
        if token.post:
            token.children.append(token.post)


def build_tree_heads(pattern, tree_heads):
    """
    Args:
        pattern: array of tokens that represents the tokens.
        tree_heads: array of tokens of the first argument.
    Returns:
        tree_heads: updated array of tokens of the first argument.
    """
    token = pattern[0]
    tree_child = token.post if token.post else None
    if isinstance(token, docopt_util.Leaf):
        in_set = False
        test_set = [t for t in tree_heads if isinstance(t, docopt_util.Leaf)]
        for test in test_set:
            if token.text == test.text:
                token = test
                in_set = True
                break
        if not in_set:
            tree_heads.append(token)
    else:
        tree_heads.append(token)
    if tree_child:
        token.children.append(tree_child)

    return tree_heads


def dict_populate_loop(pattern):
    """
    Args:
        pattern: array of tokens that represents the tokens.
    Returns:
        updated_dic: a dictionary that contains all the keywords from docstrings.
    """
    updated_dic = {}
    for token in pattern:
        if isinstance(token, docopt_util.Branch):
            updated_dic.update(dict_populate_loop(token.tokens))
        elif isinstance(token, docopt_util.SpecialToken):
            continue
        else:
            updated_dic[token.text] = token.value
    return updated_dic


def identify_tokens(pattern, options_pat):
    """
    Args:
        pattern: array of tokens that represents the tokens.
        options_pat: array of option tokens.
    Returns:
        new_pat: array of tokens that contain the updated tokens for all types of keywords.
    """
    new_pat = []
    for index, token in enumerate(pattern):
        switcher = {
            '(': docopt_util.RequiredOpen(),
            ')': docopt_util.RequiredClosed(),
            '[': docopt_util.OptionalOpen(),
            ']': docopt_util.OptionalClosed(),
            '|': docopt_util.Pipe(),
            '...': docopt_util.Repeats()
        }
        tmp_token = switcher.get(token)
        if tmp_token:
            token = tmp_token
        else:
            if (token.startswith('<') and token.endswith('>')) or token.isupper():
                token = docopt_util.Argument(token)
            elif token.startswith('--') or token.startswith('-'):
                token = get_match_option(token, options_pat)
            else:
                token = docopt_util.Command(token)

        new_pat.append(token)
    for index, token in enumerate(new_pat):
        if index == 0:
            token.post = new_pat[index + 1] if len(new_pat) > 1 else None
        elif index == len(new_pat) - 1:
            token.prev = new_pat[index - 1]
        else:
            token.prev = new_pat[index - 1]
            token.post = new_pat[index + 1]
    return new_pat


def create_opt_and_req(pattern):
    """
    Args:
        pattern: array of tokens that represents the tokens.
    """
    length = len(pattern) - 1
    for index, token in enumerate(pattern[::-1]):
        index = length - index
        if isinstance(token, (docopt_util.OptionalOpen, docopt_util.RequiredOpen)):
            closed_class = token.closed_class
            prev = token.prev if token.prev else None
            post = None
            collected = []
            del pattern[index]
            for content in pattern[index:]:
                if isinstance(content, closed_class):
                    post = content.post if content.post else None
                    del pattern[index]
                    break
                collected.append(content)
                del pattern[index]
            collected[0].prev = prev
            collected[-1].post = post
            res = docopt_util.Required(collected, prev, post) if isinstance(
                token, docopt_util.RequiredOpen) else docopt_util.Optional(collected, prev, post)
            if prev: prev.post = res
            if post: post.prev = res
            pattern.insert(index, res)


def create_mutex(pattern):
    """
    Args:
        pattern: array of tokens that represents the tokens.
    """
    for index, token in enumerate(pattern):
        if isinstance(token, (docopt_util.Optional, docopt_util.Required)):
            create_mutex(token.tokens)
        elif isinstance(token, docopt_util.Pipe):
            prev = token.prev.prev if token.prev else None
            post = token.post.post if token.post else None
            collected = [token.prev, token.post]
            for tok in collected:
                tok.prev = prev
                tok.post = post
            for _ in range(index - 1, index + 2):
                del pattern[index - 1]
            res = docopt_util.Mutex(collected, prev, post)
            pattern.insert(index - 1, res)


def create_repeating(pattern):
    """
    Args:
        pattern: array of tokens that represents the tokens
    """
    for index, token in enumerate(pattern):
        prev = token.prev if token.prev else None
        post = token.post if token.post else None
        if isinstance(token, (docopt_util.Optional, docopt_util.Required, docopt_util.Mutex)):
            create_repeating(token.tokens)
        elif isinstance(token, docopt_util.Repeats):
            token.prev.post = post
            collected = [token.prev]
            res = docopt_util.Repeating(collected, prev, post)
            for _ in range(index - 1, index + 1):
                del pattern[index - 1]
            pattern.insert(index - 1, res)


def get_match_option(token, options_pat):
    """
    Args:
        token: A string that represent the keyword for option
        options_pat: Array of option objects
    Returns:
        option: return option object if found else return None
    >>>pat = [docopt_util.Option('--help', False), docopt_util.Option('--sorted', False),
    >>> docopt_util.Option('--output', './test.txt'), docopt_util.Option('--version', False)]
    >>> get_match_option('--help', pat)
    Option('--help', False)
    >>> get_match_option('--hello', pat)
    Option('--hello', False)
    >>> get_match_option('--hi', [None])
    Option('--hi', False)
    """
    has_value = False
    if '=' in token:
        has_value = True
        token = re.search('\\S+=', token).group().strip("=")

    for option in options_pat:
        if option is None:
            return create_tmp_token(token, has_value)
        if token in (option.long, option.short):
            return option

    return create_tmp_token(token, has_value)


def create_tmp_token(token, has_value):
    """
    Args:
        token: A string that represent the keyword for option
        has_value: Boolean value for check if keyword contain value
    Returns:
        option: return option object
    >>> create_tmp_token('--hello', False)
    Option('--hello', False)
    >>> create_tmp_token('--hi', True)
    Option('--hello', True)
    """
    if token.startswith('--'):
        if has_value:
            return docopt_util.Option(text=token, value=None,
                                      has_value=has_value, short=None, long=token)
        return docopt_util.Option(token, value=False, has_value=has_value, short=None, long=token)

    if token.startswith('-'):
        if has_value:
            return docopt_util.Option(text=token, value=None,
                                      has_value=has_value, short=token, long=None)
        return docopt_util.Option(token, value=False, has_value=has_value, short=token, long=None)
    return None


def check_option_lines(options):
    """
    Args:
        options: options the options strings from docstring.
    Returns:
        new_pat: the array that holds all options objects.
    >>> check_option_lines(options= "-h --help")
    [Option('-h')]
    >>> check_option_lines(options= "hello world")
    []
    """
    options_pat = []
    for line in options:
        tmp_array = line.split()
        if len(tmp_array) > 0 and tmp_array[0].strip()[:1] != '-':
            continue
        token = None
        for count, element in enumerate(tmp_array, start=0):

            if element[:2] == '--':
                token = check_option_lines_long(element, tmp_array, count, token)
            elif element[:1] == '-':
                token = check_option_lines_short(element, tmp_array, count, token)

        token = find_default_value(line, token)
        options_pat.append(token)
    return options_pat


def check_option_lines_long(element, tmp_array, count, token):
    """
    Args:
        element: the keyword of the current option.
        tmp_array: the string the contains the current line of option description.
        count: the index of current keyword in the option line.
        token: the class object of Option that holds information of option. If object is None,
                then create a brand new object for the new keyword.
    Returns:
        token: the updated options object with long form of the keyword.
    >>> check_option_lines_long('--value=<help>', ['--value=<help>', 'Input', 'value'], 0, None)
    token = Option('--value', None, True, None, '--value')
    >>> check_option_lines_long('--value', ['--value', 'HELP'], 0, None)
    token = Option('--value', None, True, None, '--value')
    >>> check_option_lines_long('--help', ['--help', 'show', 'help', 'message'], 0, None)
    token = Option(''--help', False, False, None, ''--help')
    """
    if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        if token is None:
            token = docopt_util.Option(element, value=None,
                                       has_value=True, short=None, long=element)
        else:
            token.long = element
            token.text = element
    elif '=' in element:
        if token is None:
            text = re.search('\\S+=', element).group().strip("=")
            token = docopt_util.Option(text, value=None, has_value=True, short=None, long=text)
        else:
            token.long = re.search('\\S+=', element).group().strip("=")
            token.text = re.search('\\S+=', element).group().strip("=")
    else:
        if token is None:
            token = docopt_util.Option(element, value=False,
                                       has_value=False, short=None, long=element)
        else:
            token.long = element
            token.text = element
    return token


def check_option_lines_short(element, tmp_array, count, token):
    """
    Args:
        element: the keyword of the current option.
        tmp_array: the string the contains the current line of option description.
        count: the index of current keyword in the option line.
        token: the class object of Option that holds information of option.
    Returns:
        token: the updated options object with short form of the keyword.
    >>> check_option_lines_long('-v=<help>', ['-v=<help>', 'Input', 'value'], 0, None)
    token = Option('-v', None, True, '-v', None)
    >>> check_option_lines_long('-v', ['-v', 'HELP'], 0, None)
    token = Option('-v', None, True, '-v', None)
    >>> check_option_lines_long('-h', ['-h', 'show', 'help', 'message'], 0, None)
    token = Option('-h', False, False, '-h', None)
    """
    if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        if token is None:
            token = docopt_util.Option(element, value=None, has_value=True, short=element,
                                       long=None)
        else:
            token.short = element
    elif '=' in element:
        if token is None:
            text = re.search('\\S+=', element).group().strip("=")
            token = docopt_util.Option(text, value=None, has_value=True, short=text, long=None)
        else:
            token.short = re.search('\\S+=', element).group().strip("=")
    else:
        if token is None:
            token = docopt_util.Option(element, value=False, has_value=False, short=element,
                                       long=None)
        else:
            token.short = element
    return token


def find_default_value(line, token):
    """
    Args:
        line: a string that holds the current line.
        token: The toekn object for holding option.
    Returns:
        token: the updated token accroding the existence of default value
    >>> tmp_token = docopt_util.Option('-v', None, True, '-v', None)
    >>> find_default_value('-v FILE  input file [default: ./test.txt].', tmp_token)
    tmp_token = Option('-v', './test.txt', True, '-v', None)
    >>> tmp_token = docopt_util.Option('--location', None, True, '-l', '--location')
    >>> find_default_value('-l=<location_value>  insert coordinate [default: 10.88].', tmp_token)
    tmp_token = Option('--location', 10.88, True, '-l', '--location')
    """

    matching = re.search(r'\[.*?]', line)
    if matching is not None:
        default_value = matching.group(0)[1:-1].strip()

        # Test if this line of docstring contains a default value
        if re.search('default:', default_value, re.IGNORECASE):
            try:
                int(default_value.split()[1])
                token.value = int(default_value.split()[1])
            except ValueError:
                try:
                    float(default_value.split()[1])
                    token.value = float(default_value.split()[1])
                except ValueError:
                    token.value = default_value.split()[1]
    return token


# A helper function for display a nice looking dictionary to the user
def output_formatter(rows, length, dic_list, dictionary_total):
    """
    Args:
        rows: count for how many rows needed for output dictionary.
        length: the total length for the output usage and options dictionary.
        dic_list: reformat the dictionary into a array.
        dictionary_total: combined dictionary (usage dic + options dic).
    Returns:
        returns the string from display or an array for testing.
    >>> dic = {'--helping': True, '--sorted': True, '--output': 'ttt.pdf', '--version': False,
    >>>        '--speed': 10, '--moored': True, '--drifting': None, '--rr': False, '--aaa': 20.9,
    >>>        '--yyy': False}
    >>> d_list = list(dic)
    >>> output_formatter(rows=4, length=len(dic_list), dic_list=dic_list, dictionary_total=dic)
    "{'--helping': True         '--speed': 10          '--aaa': 20.9\n" + \
    " '--sorted': True          '--moored': True       '--yyy': False\n" + \
    " '--output': 'ttt.pdf'     '--drifting': None\n" + \
    " '--version': False        '--rr': False}\n"
    """

    col1 = [' '] * rows
    col2 = [' '] * rows
    col3 = [' '] * rows
    for i in range(0, rows):
        if length > i:
            col1[i] += insert_content(dic_list, i, rows, 0, dictionary_total)
        if length > i + rows:
            col2[i] += insert_content(dic_list, i, rows, 1, dictionary_total)
        if length > i + (2 * rows):
            col3[i] += insert_content(dic_list, i, rows, 2, dictionary_total)

    return print_output_from_rows(col1, col2, col3, rows)


# Helper function for inserting the key value pairs into output dictionary
def insert_content(dic_list, idx, rows, col_idx, dictionary_total):
    """
    Args:
        dic_list:  a dictionary the built from user argument but reform to a list.
        idx: the current row index.
        rows: count of the rows.
        col_idx: index of the col,
        dictionary_total: the dictionary that includes both keywords for output patterns
                          and options.
    Returns:
        returns the key value pair in a outputting form according to the type of values.
    >>> dic = {'--helping': True, '--sorted': None, '--output': 'ttt.pdf',
    >>>        '--speed': 10, '--aaa': 20.9}
    >>> d_list = list(dic)
    >>> insert_content(dic_list=dic_list, idx=0, rows=0, col_idx=0, dictionary_total=dic)
    '--helping: True'
    >>> insert_content(dic_list=dic_list, idx=1, rows=0, col_idx=0, dictionary_total=dic)
    '--sorted: None'
    >>> insert_content(dic_list=dic_list, idx=2, rows=0, col_idx=0, dictionary_total=dic)
    '--output: ttt.pdf'
    >>> insert_content(dic_list=dic_list, idx=3, rows=0, col_idx=0, dictionary_total=dic)
    '--speed: 10'
    >>> insert_content(dic_list=dic_list, idx=4, rows=0, col_idx=0, dictionary_total=dic)
    '--aaa: 20.9'
    """

    if check_value_type(dictionary_total[dic_list[idx + (col_idx * rows)]]):
        return '\'{}\': {}'.format(dic_list[idx + (col_idx * rows)],
                                   dictionary_total[dic_list[idx + (col_idx * rows)]])

    return '\'{}\': \'{}\''.format(dic_list[idx + (col_idx * rows)],
                                   dictionary_total[dic_list[idx + (col_idx * rows)]])


# Helper method for defining whether the value is a string or a primitive type
def check_value_type(value):
    """
    Args:
        value: the value for current key in the dictionary.
    Returns:
        returns a boolean value whether the value passed in is primitive.
    >>> check_value_type('Perfect')
    False
    >>> check_value_type(10)
    True
    >>> check_value_type(3.1415)
    True
    >>> check_value_type(True)
    True
    >>> check_value_type(None)
    True
    """

    return isinstance(value, (int, float, bool)) or value is None


# Helper method for printing out dictionary as a json string to user
def print_output_from_rows(col1, col2, col3, num_rows):
    """
    Args:
        col1: holds the values for output column one.
        col2: holds the values for output column two.
        col3: holds the values for output column three.
        num_rows: the number of rows
    Returns:
        final_output: returns output string
    >>> first_row = [' 11', ' 2', ' 3', ' 4', ' 5']
    >>> second_row = [' 1', ' 222', ' 3', ' 4', ' ']
    >>> third_row = [' 1', ' 2', ' 3333', ' ', ' ']
    >>> print_output_from_rows(col1=col1, col2=col2, col3=col3, num_rows=5)
    "{11     1       1\n" + \
    " 2      222     2\n" + \
    " 3      3       3333\n" + \
    " 4      4\n" + \
    " 5}\n"
    """
    col1 = [i for i in col1 if len(i) > 1]
    num_rows = min(len(col1), num_rows)
    spaces1 = len(max(col1, key=len))
    spaces2 = len(max(col2, key=len))
    final_output = ""
    for k in range(num_rows):
        if k == 0:
            out = '{' + col1[k].strip().ljust(spaces1) + ' ' * 4 \
                  + col2[k].strip().ljust(spaces2) + ' ' * 4 \
                  + col3[k].strip().ljust(spaces2)
        else:
            out = col1[k].ljust(spaces1) + ' ' * 4 \
                  + col2[k].ljust(spaces2) + ' ' * 4 \
                  + col3[k].ljust(spaces2)
        if k == num_rows - 1:
            final_output += (out.rstrip() + '}\n')
        else:
            final_output += (out.rstrip() + '\n')
    return final_output
