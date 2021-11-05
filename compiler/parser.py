import pprint

from betterLogger import ClassWithLogger, push_name_to_logger_name_stack, get_logger

from compiler.grammar import callOpenOperator, callCloseOperator
from compiler.structures import Token, Node
from compiler.token_types import NEWLINE, OPERATOR, IDENTIFIER, INTEGER


class Parser(ClassWithLogger):
    current_location: int = 0
    tokens: list[Token]

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

        self.current_location = 0
        while self.current_location < len(self.tokens):
            self.log_dump(f"Current location is {self.current_location} which is "
                          f"\"{self.tokens[self.current_location]}\"")

            line_tokens = self.get_from_current_location_to_newline()
            node = parse(line_tokens, logger=self)
            print(node)

    def get_from_current_location_to_newline(self):
        return get_tokens_until_end(self.tokens, NEWLINE, "token_type", start=self.current_location)


def parse(tokens, logger=None):
    if logger is None:
        logger = get_logger("Parser")


    if len(tokens) == 1:  # Simple ints and ids ect
        if tokens[0].is_type(INTEGER):
            logger.log_dump("Identified token as an integer")
            return tokens[0]

    elif tokens[1] == (OPERATOR, callOpenOperator):
        if not tokens[0].is_type(IDENTIFIER):
            logger.log_error(f"Identified tokens as a call but first token is not an Identifier | tokens=\n"
                             f"{pprint.pformat(tokens)}")
        logger.log_dump("Identified tokens as a call")
        node = Node(type=tokens[1], contents=[tokens[0],
                                              parse(get_tokens_until_end(tokens[2:], (OPERATOR, callCloseOperator),
                                                                         "token_values"), logger=logger)])
        return node

    else:
        logger.log_error("Could not identify what tokens mean | tokens=\n"
                             f"{pprint.pformat(tokens)}")


def get_tokens_until_end(tokens, end, end_type, start=0):
    ret = list()

    n = 0 + start
    while not ((end_type == "token_type" and tokens[n].is_type(end)) or
               (end_type == "token_values" and tokens[n] == end)):
        ret.append(tokens[n])
        n += 1
    return ret
