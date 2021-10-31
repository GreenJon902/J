import pprint

from betterLogger import ClassWithLogger, push_name_to_logger_name_stack

from compiler.structures import Token
from compiler.token_types import IDENTIFIER, OPERATOR


class Parser(ClassWithLogger):
    tokens: list[Token]
    file_path: str
    current_location: int = 0


    def __init__(self, tokens, metadata: dict = None):
        ClassWithLogger.__init__(self)

        if metadata is None:
            metadata = {}
        self.file_path = metadata.pop("file_path", "UnnamedFile")

        self.tokens = tokens

        self.push_logger_name(f"\"{self.file_path}\"")


    @push_name_to_logger_name_stack
    def get_ast(self):
        self.log_debug("Getting ast for self")
        self.log_trace(f"Tokens are:\n{pprint.pformat(self.tokens)}")
        ast = list()

        self.current_location = 0
        while self.current_location < len(self.tokens):
            self.log_dump(f"Current location is {self.current_location} which is "
                          f"\"{self.tokens[self.current_location]}\"")
            self.current_location += 1
