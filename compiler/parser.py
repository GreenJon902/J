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

        nodes = []

        self.current_location = 0
        while self.current_location < len(self.tokens):
            self.log_dump(f"Current location is {self.current_location} which is "
                          f"\"{self.tokens[self.current_location]}\"")

            line_tokens = self.get_from_current_location_to_newline()
            node = parse(line_tokens, logger=self)
            self.log_dump(f"Got \n{node}")
            nodes.append(node)
            self.current_location += len(line_tokens) + 1

        self.log_debug(f"AST is \n{''.join([str(node) for node in nodes])}")
        return nodes

    def get_from_current_location_to_newline(self):
        return get_tokens_until_end(self.tokens, NEWLINE, "token_type", start=self.current_location)


def parse(tokens, logger=None):
    if logger is None:
        ln = False
        logger = get_logger("Parser")
    else:
        ln = True
        logger.push_logger_name("<.parse()")

    ast = None
    current_location = 0
    while current_location < len(tokens):
        logger.log_dump(f"Current location is {current_location} which is "
                        f"\"{tokens[current_location]}\"")

        if tokens[current_location].is_type(IDENTIFIER):
            logger.log_debug("Current location identified as identifier")
            ast = tokens[current_location]
            current_location += 1

        elif tokens[current_location] == (OPERATOR, callOpenOperator):
            logger.log_debug("Current location identified as call")

            logger.push_logger_name(str(current_location))
            args_tokens = get_tokens_until_end(tokens[2:], end=(OPERATOR, callCloseOperator), end_type="token_values")
            args = parse(args_tokens, logger=logger)
            logger.pop_logger_name()
            ast = Node(type="callIdentifier", left=ast, right=args)

            current_location += 1 + len(args_tokens) + 1

        elif tokens[current_location].is_type(INTEGER):
            logger.log_debug("Current location identified as integer")
            ast = tokens[current_location]
            current_location += 1


    if ln:
        logger.pop_logger_name()
    return ast


def get_tokens_until_end(tokens, end, end_type, start=0):
    ret = list()

    n = 0 + start
    while not ((end_type == "token_type" and tokens[n].is_type(end)) or
               (end_type == "token_values" and tokens[n] == end)):
        ret.append(tokens[n])
        n += 1
    return ret
