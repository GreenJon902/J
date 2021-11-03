from compiler.token_types import IDENTIFIER, OPERATOR, INTEGER, NEWLINE


class Token:
    type: str
    contents: str

    # noinspection PyShadowingBuiltins
    def __init__(self, type, contents):
        self.type = type
        self.contents = contents

    def __repr__(self):
        return f"Token(type={self.type}, contents=\"{self.contents}\")"

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


class NoneGenericToken(Token):
    def __init__(self, contents):
        Token.__init__(self, self.__class__.__name__, contents)

    def __repr__(self):
        return f"{self.__class__.__name__}(contents=\"{self.contents}\")"


class IdentifierToken(NoneGenericToken):
    pass


class OperatorToken(NoneGenericToken):
    pass


class IntegerToken(NoneGenericToken):
    pass


class NewlineToken(Token):
    def __init__(self):
        Token.__init__(self, self.__class__.__name__, None)

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
