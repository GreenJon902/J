import pprint

from betterLogger import ClassWithLogger, push_name_to_logger_name_stack

from compiler.grammar import getAttributeOperator, callOpenOperator, callCloseOperator, arithmeticOperators
from compiler.structures import Token, Node
from compiler.token_types import IDENTIFIER, OPERATOR, NEWLINE, INTEGER


class Parser(ClassWithLogger):
    tokens: list[Token]
    file_path: str
    current_location: int = 0
    amount_to_skip: int = 0


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
        current_node = Node(type="Line")
        ast.append(current_node)

        self.current_location = 0
        while self.current_location < len(self.tokens):
            self.log_dump(f"Current location is {self.current_location} which is "
                          f"\"{self.tokens[self.current_location]}\"")

            # Get attr -------------------------------------------------------------------------------------------------
            if (self.tokens[self.current_location].type == IDENTIFIER
                    and self.tokens[self.current_location + 1].type == OPERATOR
                    and self.tokens[self.current_location + 1].contents == getAttributeOperator
                    and self.tokens[self.current_location + 2].type == IDENTIFIER):
                self.log_debug("Current location identified as getAttribute")

                getAttributeNode = Node(self.tokens[self.current_location + 1], [])
                node = Node(self.tokens[self.current_location], [getAttributeNode])
                self.log_debug(f"New Node is\n{node}")
                current_node.contents.append(node)
                current_node = getAttributeNode
                self.bump_current_location(2)


            # Get call function ----------------------------------------------------------------------------------------
            elif (self.tokens[self.current_location].type == IDENTIFIER
                    and self.tokens[self.current_location + 1].type == OPERATOR
                    and self.tokens[self.current_location + 1].contents == callOpenOperator):
                self.log_debug("Current location identified as call")


                token_before_bump_and_parse_expression = self.tokens[self.current_location]

                self.bump_current_location(2)
                arguments_ast = self.parse_expression(special_end=callCloseOperator)
                self.log_dump(f"Got list of arguments as ast: \n{arguments_ast}")

                node = Node(token_before_bump_and_parse_expression, [arguments_ast])
                self.log_debug(f"New Node is\n{node}")
                current_node.contents.append(node)
                current_node = node

            elif self.tokens[self.current_location].type == NEWLINE:
                self.log_debug(f"Line was:\n{''.join([str(node) for node in ast])}")
                self.bump_current_location(1)
                current_node = Node(type="Line")
                ast.append(current_node)

            else:
                self.log_critical(f"Could not identify what the tokens at {self.current_location} meant")
                self.bump_current_location(1)  # FIXME: This is for testing


    def parse_expression(self, special_end=NEWLINE):
        self.push_logger_name(f"parse_expression({self.current_location})")
        self.log_dump(f"Parsing Expression at {self.current_location} which is "
                      f"\"{self.tokens[self.current_location]}\"")


        # Expression end
        if self.tokens[self.current_location].type == special_end or \
                self.tokens[self.current_location].contents == special_end:
            ret = None

        # Arithmetic
        elif (self.tokens[self.current_location].type == INTEGER
                and self.tokens[self.current_location + 1].type == OPERATOR
                and self.tokens[self.current_location + 1].contents in arithmeticOperators):
            if (self.tokens[self.current_location + 2].type == INTEGER
                    and (self.tokens[self.current_location + 3].type == special_end
                            or self.tokens[self.current_location + 3].contents == special_end)):
                ret = Node(self.tokens[self.current_location + 1],
                           (self.tokens[self.current_location], self.tokens[self.current_location + 2]))
                self.bump_current_location(4)

            else:
                ret = None  # TODO: This

        else:
            self.log_error(f"Could not identify what the tokens at {self.current_location} meant")
            ret = None


        self.log_trace(f"Returning \n{ret}")
        self.pop_logger_name()
        return ret


    def bump_current_location(self, amount):
        self.log_trace(f"Skipping {amount}")
        self.current_location += amount
