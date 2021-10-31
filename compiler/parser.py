from betterLogger import ClassWithLogger


class Parser(ClassWithLogger):
    tokens: list[tuple[str, str]]
    file_path: str
    current_location: int = 0

    def __init__(self, tokens, file_path):
        ClassWithLogger.__init__(self)

        self.tokens = tokens
        self.file_path = file_path

        self.push_logger_name(f"\"{self.file_path}\"")

    def get_ast(self):
        pass
