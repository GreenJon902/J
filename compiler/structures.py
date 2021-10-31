class Token:
    type: str
    contents: str

    # noinspection PyShadowingBuiltins
    def __init__(self, type, contents):
        self.type = type
        self.contents = contents

    def __repr__(self):
        return f"Token(type={self.type}, contents=\"{self.contents}\")"
