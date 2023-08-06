"""
  This module is for holding all the class objects which used to create the tokens
  for each type of keywords in the usage pattern and options table in the docstrings
"""
import re


class DocoptExit(Exception):
    """
    Exception class for docopt
    """

    def __init__(self, message="Exception occur."):
        self.message = message
        super().__init__(self.message)


class Token:
    """
    class token is the parent class for all different tokens
    """

    def __init__(self, prev=None, post=None, children=None):
        """
        :param prev: the prev level node
        :param post: the next following node
        :param children: the list of tokens
        """
        if children is None:
            children = []
        self.prev = prev
        self.post = post
        self.children = children
        self.index = 0

    @property
    def name(self):
        """
        :return: "Token"
        """
        return "Token"

    @property
    def get_class(self):
        """
        :return: class type
        """
        return Token


# pylint: disable=too-many-arguments
class Leaf(Token):
    """
    class leaf
    """

    def __init__(self, text, value=None, prev=None, post=None, children=None):
        """

        :param text: the keyword for leaf token
        :param value: the value of this token
        :param prev: the prev object
        :param post: the next linked object
        :param children: the list of children of current keyword token
        """
        self.text = text
        self.value, self.prev, self.post, self.children = (value, prev, post, children)
        if self.children is None:
            self.children = []
        super().__init__(self.prev, self.post, self.children)
        self.index = 0

    def __repr__(self):
        """
        :return: return the formatted string of leaf
        """
        return '%s(%r, %r)' % (self.__class__.__name__, self.text, self.value)

    def flat(self, *types):
        """

        :param types: check the type of argument
        :return: return self is argument is self type else return None
        """
        return self if not types or type(self) in types else None


class Argument(Leaf):
    """ Placeholder """

    def __init__(self, text, prev=None, post=None, children=None):
        """
            :param text: the keyword of current node
            :param prev: the prev level node
            :param post: the next following node
            :param children: the list of tokens
            """
        if children is None:
            children = []
        self.value = None if len(text.strip("<>")) > 1 else 0
        super().__init__(text, value=self.value, prev=prev, post=post, children=children)
        self.index = 2

    def match(self, args, index):
        """

        :param args: the list of tokens for comparison
        :param index: the index of token that will be compared
        :return: return true, the next index of token list, and the dictionary if success
        """
        is_match = False
        if index < len(args):
            if self.value != 0 or is_num(args[index]):
                self.value, is_match = args[index], True
        res_dict = self.get_res_dict(is_match)
        return is_match, index + 1, res_dict

    def get_res_dict(self, is_match):
        """

        :param is_match: boolean for if input is matching the pattern
        :return: return the dictionary is success
        """
        if not is_match:
            return dict()
        return dict({self.text: self.value})


# pylint: disable=too-many-arguments
class Option(Leaf):
    """ Placeholder """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, text, value=None, has_value=False, short=None,
                 long=None, prev=None, post=None, children=None):
        self.text = text
        self.value = value
        self.has_value = has_value
        self.short = short
        self.long = long
        self.prev = prev
        self.post = post
        self.children = children
        if self.children is None:
            self.children = []
        if '=' in text:
            arg = re.search('<\\S+>', text).group()
            text = re.search('\\S+=', text).group().strip("=")
            self.value = None if len(arg.strip("<>")) > 1 else 0
        else:
            self.value = None if '=' in text else False
        super().__init__(text, value=self.value, prev=self.prev,
                         post=self.post, children=self.children)
        self.index = 3

    def match(self, args, index):
        """

        :param args: the list of incoming argument that will be used to compare
        :param index: the index of element that needed to compare
        :return: return true and the new index skipping to and the dictionary for current keyword
        """
        is_match = False
        new_index = index + 1
        if index < len(args):
            if self.text == args[index]:
                if self.has_value:
                    if index + 1 < len(args):
                        self.value = args[index + 1]
                        is_match = True
                        new_index = index + 2
                else:
                    self.value = True
                    is_match = True
        res_dict = self.get_res_dict(is_match)
        return is_match, new_index, res_dict

    def get_res_dict(self, is_match):
        """

        :param is_match: boolean value for checking if the token is matching argument
        :return: return the dictionary according to the boolean
        """
        if not is_match:
            return dict()
        return dict({self.text: self.value})


# pylint: disable=too-many-arguments
class Command(Leaf):
    """ Placeholder """

    def __init__(self, text, value=False, prev=None, post=None, children=None):
        """
            :param text: the keyword of current node
            :param prev: the prev level node
            :param post: the next following node
            :param children: the list of tokens
        """
        if children is None:
            children = []
        self.value = value
        super().__init__(text, value=self.value, prev=prev, post=post, children=children)
        self.index = 1

    def match(self, args, index):
        """
        :param args: the list of incoming argument that will be used to compare
        :param index: the index of element that needed to compare
        :return: return true and the new index skipping to and the dictionary for current keyword
        """
        is_match = False
        if index < len(args):
            if self.text == args[index]:
                self.value, is_match = True, True
        res_dict = self.get_res_dict(is_match)
        return is_match, index + 1, res_dict

    def get_res_dict(self, is_match):
        """

        :param is_match: boolean value for checking if the token is matching argument
        :return: return the dictionary according to the boolean
        """
        if not is_match:
            return dict()
        return dict({self.text: True})


# Used for grouping Tokens by optional, required, mutex, or repeating
class Branch(Token):
    """Branch class"""

    def __init__(self, tokens=None, prev=None, post=None, children=None):
        """

        :param tokens: the list of tokens of current branch
        :param prev: the previous linked object
        :param post: the post linked object
        :param children: the list of tokens
        """
        if children is None:
            children = []
        if tokens is None:
            tokens = []
        self.tokens = tokens
        super().__init__(prev, post, children)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join(repr(a) for a in self.tokens))

    def flat(self, *types):
        """

        :param types: the class type of current keyword
        :return: return all the children's class type
        """
        if type(self) in types:
            return self
        return [child.flat(*types) for child in self.tokens]


class Optional(Branch):
    """ Placeholder """

    def match(self, args, index):
        """
        :param args: the list of incoming argument that will be used to compare
        :param index: the index of element that needed to compare
        :return: return true and the new index skipping to and the dictionary for current keyword
        """
        is_match, child_index, res_dict = True, index, dict()
        for child in self.tokens:
            old_index = child_index
            is_match, child_index, child_dict = child.match(args, child_index)
            if not is_match:
                child_index = old_index
            else:
                res_dict.update(child_dict)

        return True, child_index, res_dict


class Required(Branch):
    """ Placeholder """

    def match(self, args, index):
        """
        :param args: the list of incoming argument that will be used to compare
        :param index: the index of element that needed to compare
        :return: return true and the new index skipping to and the dictionary for current keyword
        """
        is_match, child_index, res_dict = True, index, dict()
        for child in self.tokens:
            old_index = child_index
            is_match, child_index, child_dict = child.match(args, child_index)

            if not is_match:
                child_index = old_index
            res_dict.update(child_dict)
        return is_match, child_index, res_dict


class Mutex(Branch):
    """ Placeholder """

    def match(self, args, index):
        """
        :param args: the list of incoming argument that will be used to compare
        :param index: the index of element that needed to compare
        :return: return true and the new index skipping to and the dictionary for current keyword
        """
        is_match, new_index, res_dict = False, index, dict()
        for child in self.tokens:
            is_match, new_index, temp_dict = child.match(args, index)
            if is_match:
                res_dict = temp_dict
                break
        return is_match, new_index, res_dict


class Repeating(Branch):
    """ Placeholder """

    # BUG: index 1 less than it should be when repeating pattern incomplete
    def match(self, args, index):
        """
        :param args: the list of incoming argument that will be used to compare
        :param index: the index of element that needed to compare
        :return: return true and the new index skipping to and the dictionary for current keyword
        """
        res_dict_full = dict()
        res_list = []
        is_match, new_index, res_dict_item = self.tokens[0].match(args, index)
        res_list.append(res_dict_item)
        if not is_match:
            return False, new_index, dict()
        while new_index < len(args):
            is_match, new_index, res_dict_item = self.tokens[0].match(
                args, new_index)
            if not is_match:
                new_index = new_index - 1
                break
            res_list.append(res_dict_item)
        for item in res_list:
            for key, val in zip(item.keys(), item.values()):
                if key in res_dict_full.keys():
                    if not isinstance(res_dict_full[key], list):
                        res_dict_full[key] = [res_dict_full[key]]
                    res_dict_full[key].append(val)
                else:
                    res_dict_full[key] = [val]
        return True, new_index, res_dict_full


class SpecialToken(Token):
    """ Placeholder"""

    def __init__(self, prev=None, post=None, children=None):
        """

        :param prev: the prev linked node
        :param post: the next linked node
        :param children: the list of tokens for holding the children nodes
        """
        if children is None:
            children = []
        super().__init__(prev, post, children)

    @property
    def name(self):
        """
        :return: "SpecialToken"
        """
        return "SpecialToken"

    @property
    def get_class(self):
        """
        :return: class type
        """
        return SpecialToken


class OptionalOpen(SpecialToken):
    """ Placeholder """

    @property
    def closed_class(self):
        """

        :return: optional closed class type token
        """
        return OptionalClosed

    @property
    def name(self):
        """
        :return: "OptionalOpen"
        """
        return "OptionalOpen"

    @property
    def get_class(self):
        """
        :return: class type
        """
        return OptionalOpen


class OptionalClosed(SpecialToken):
    """ Placeholder """

    @property
    def name(self):
        """
        :return: "OptionalClosed"
        """
        return "OptionalClosed"

    @property
    def get_class(self):
        """
        :return: class type
        """
        return OptionalClosed


class RequiredOpen(SpecialToken):
    """ Placeholder """

    @property
    def closed_class(self):
        """
        :return: Required closed class token
        """
        return RequiredClosed

    @property
    def name(self):
        """
        :return: "RequiredOpen"
        """
        return "RequiredOpen"

    @property
    def get_class(self):
        """
        :return: class type
        """
        return RequiredOpen


class RequiredClosed(SpecialToken):
    """ Placeholder """

    @property
    def name(self):
        """
        :return: "RequiredClosed"
        """
        return "RequiredClosed"

    @property
    def get_class(self):
        """
        :return: class type
        """
        return RequiredClosed


class Pipe(SpecialToken):
    """ Placeholder """

    @property
    def name(self):
        """
        :return: "Pipe"
        """
        return "Pipe"

    @property
    def get_class(self):
        """
        :return: class type
        """
        return Pipe


class Repeats(SpecialToken):
    """ Placeholder """

    @property
    def name(self):
        """
        :return: "Repeats"
        """
        return "Repeats"

    @property
    def get_class(self):
        """
        :return: class type
        """
        return Repeats


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
