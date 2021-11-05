from compiler.token_types import IDENTIFIER, OPERATOR, INTEGER, NEWLINE


class Token:
    type: str
    content: str

    # noinspection PyShadowingBuiltins
    def __init__(self, type, contents):
        self.type = type
        self.content = contents

    def __repr__(self):
        return f"Token(type={self.type}, content=\"{self.content}\")"

    @classmethod
    def new(cls, token_type, token_value):
        if token_type == IDENTIFIER:
            return IdentifierToken(token_value)
        elif token_type == OPERATOR:
            return OperatorToken(token_value)
        elif token_type == INTEGER:
            return IntegerToken(token_value)
        elif token_type == NEWLINE:
            return NewlineToken()
        else:
            return Token(token_type, token_value)

    def is_type(self, other):
        return self.type == other

    def __eq__(self, other):
        return self.type == other[0] and self.content == other[1]


class NoneGenericToken(Token):
    type_name = None

    def __init__(self, contents):
        Token.__init__(self, self.type_name, contents)

    def __repr__(self):
        return f"{self.__class__.__name__}(content=\"{self.content}\")"


class IdentifierToken(NoneGenericToken):
    type_name = IDENTIFIER


class OperatorToken(NoneGenericToken):
    type_name = OPERATOR


class IntegerToken(NoneGenericToken):
    type_name = INTEGER


class NewlineToken(Token):
    def __init__(self):
        Token.__init__(self, NEWLINE, None)

    def __repr__(self):
        return f"NewlineToken()"


new_line = "\n"


class Node:
    type: Token
    contents: list[Token]

    # noinspection PyShadowingBuiltins
    def __init__(self, type, contents=None):
        if contents is None:
            contents = []
        self.type = type
        self.contents = contents

    def __repr__(self):
        return f"Node(type={repr(self.type)}, contents=\"{repr(self.contents)}\")"

    def __str__(self, indent=0):
        return f"{self.type}:\n" + "".join([("    " * (indent + 1)) + ((child.__str__(indent=indent + 1) if
                                                                        isinstance(child, Node) else str(child)) +
                                                                       new_line) for child in self.contents]).\
            removesuffix("\n")
