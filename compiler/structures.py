class Token:
    type: str
    contents: str

    # noinspection PyShadowingBuiltins
    def __init__(self, type, contents):
        self.type = type
        self.contents = contents

    def __repr__(self):
        return f"Token(type={self.type}, contents=\"{self.contents}\")"


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
