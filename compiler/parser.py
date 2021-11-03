import pprint

from betterLogger import ClassWithLogger, push_name_to_logger_name_stack

from compiler.grammar import getAttributeOperator, callOpenOperator, callCloseOperator, argumentSeparatorOperator
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

        fileNode = Node(type=f"\"{self.file_path}\"")
        current_node = fileNode

        self.current_location = 0
        while self.current_location < len(self.tokens):
            self.log_dump(f"Current location is {self.current_location} which is "
                          f"\"{self.tokens[self.current_location]}\"")

            # Identifier -----------------------------------------------------------------------------------------------
            if self.tokens[self.current_location].type == IDENTIFIER:
                self.log_debug("Current location identified as identifier")

                node = Node(self.tokens[self.current_location], [])
                self.log_debug(f"New Node is\n{node}")
                current_node.contents.append(node)
                current_node = node
                self.bump_current_location(1)


            # Get attr -------------------------------------------------------------------------------------------------
            elif (self.tokens[self.current_location - 1].type == IDENTIFIER
                    and self.tokens[self.current_location].type == OPERATOR
                    and self.tokens[self.current_location].contents == getAttributeOperator
                    and self.tokens[self.current_location + 1].type == IDENTIFIER):
                self.log_debug("Current location identified as getAttribute")

                getAttributeNode = Node(self.tokens[self.current_location + 1], [])
                node = Node(self.tokens[self.current_location], [getAttributeNode])
                self.log_debug(f"New Node is\n{node}")
                current_node.contents.append(node)
                current_node = getAttributeNode
                self.bump_current_location(2)


            # Get call function ----------------------------------------------------------------------------------------
            elif (self.tokens[self.current_location - 1].type == IDENTIFIER
                    and self.tokens[self.current_location].type == OPERATOR
                    and self.tokens[self.current_location].contents == callOpenOperator):
                self.log_debug("Current location identified as call")


                self.bump_current_location(1)
                arguments_ast = self.parse_expression(special_ends=(callCloseOperator, argumentSeparatorOperator))
                self.log_dump(f"Got list of arguments as ast: \n{arguments_ast}")

                node = arguments_ast
                self.log_debug(f"New Node is\n{node}")
                current_node.contents.append(node)
                current_node = node


            # Newline --------------------------------------------------------------------------------------------------
            elif self.tokens[self.current_location].type == NEWLINE:
                current_node = fileNode
                self.log_dump(f"Finished line")
                self.bump_current_location(1)

            else:
                self.log_critical(f"Could not identify what the tokens at {self.current_location} meant")
                self.bump_current_location(1)  # FIXME: This is for testing

        self.log_debug(f"Got ast:\n{fileNode}")
        return fileNode

    def parse_expression(self, special_ends: tuple[str, ] = None):
        if special_ends is None:
            special_ends = (NEWLINE,)
        self.push_logger_name(f"parse_expression({self.current_location})")
        self.log_dump(f"Parsing Expression at {self.current_location} which is "
                      f"\"{self.tokens[self.current_location]}\"")

        left = None
        operator = None
        right = None
        while True:
            if self.tokens[self.current_location].type in special_ends or \
                    self.tokens[self.current_location].contents in special_ends:  # End --------------------------------
                self.log_trace(f"Expression ended at {self.current_location}")
                self.bump_current_location(1)
                break

            elif self.tokens[self.current_location].type != OPERATOR:  # Left ------------------------------------------
                self.log_trace(f"Found a left side at {self.current_location}")

                if self.tokens[self.current_location].type == INTEGER:
                    left = self.tokens[self.current_location]
                    self.log_trace(f"Left side at {self.current_location} was an integer that was {left}")
                    self.bump_current_location(1)

            else:  # Operator and right --------------------------------------------------------------------------------
                self.log_trace(f"Found a right side at {self.current_location}")

                if self.tokens[self.current_location + 1].type == INTEGER:
                    operator = self.tokens[self.current_location]
                    right = self.tokens[self.current_location + 1]

                    self.log_trace(f"Right side at {self.current_location} was an operator that was {operator} and the "
                                   f"trailing integer was {right}")

                    self.bump_current_location(2)


        if left is None:
            ret = None

        elif operator is None:
            ret = left

        else:
            ret = Node(operator, [left, right])

        self.log_trace(f"Returning \n{ret}")
        self.pop_logger_name()
        return ret


    def bump_current_location(self, amount):
        self.log_trace(f"Skipping {amount}")
        self.current_location += amount
