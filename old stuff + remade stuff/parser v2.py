import pprint

from betterLogger import ClassWithLogger, push_name_to_logger_name_stack

from compiler.grammar import getAttributeOperator, callOpenOperator, callCloseOperator
from compiler.structures import Node, Token
from compiler.token_types import NEWLINE, IDENTIFIER, OPERATOR, INTEGER


class Parser(ClassWithLogger):
    current_location: int = 0
    tokens: list[Token]
    file_path: str

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

        rootNode = Node(type="RootNode")
        current_node = rootNode

        self.current_location = 0
        while self.current_location < len(self.tokens):
            self.push_logger_name(str(self.current_location))
            self.log_dump(f"Current location is {self.current_location} which is "
                          f"\"{self.tokens[self.current_location]}\"")

            current_node.contents.append(self.parse_until(NEWLINE))

            self.pop_logger_name()

    def parse_until(self, end):
        self.push_logger_name(f"parse_until({self.current_location})")
        self.log_dump(f"Parsing Expression at {self.current_location} which is "
                      f"\"{self.tokens[self.current_location]}\" until {end}")

        rootNode = Node(type="RootNode")
        current_node = rootNode

        reached_end = False
        while not reached_end:
            if self.tokens[self.current_location] == end:
                self.log_trace(f"Reached end at {self.current_location}")
                self.bump_current_location(1)
                print(rootNode)
                reached_end = True

            # Identifier -----------------------------------------------------------------------------------------------
            if self.tokens[self.current_location] == IDENTIFIER:
                self.log_debug("Current location identified as identifier")

                node = Node(self.tokens[self.current_location])
                self.log_debug(f"New Node is\n{node}")
                current_node.contents.append(node)
                current_node = node
                self.bump_current_location(1)


            # Get attr -------------------------------------------------------------------------------------------------
            elif (self.tokens[self.current_location - 1] == IDENTIFIER
                  and self.tokens[self.current_location].is_a(getAttributeOperator)
                  and self.tokens[self.current_location + 1] == IDENTIFIER):
                self.log_debug("Current location identified as getAttribute")

                getAttributeNode = Node(self.tokens[self.current_location + 1])
                node = Node(self.tokens[self.current_location], [getAttributeNode])
                self.log_debug(f"New Node is\n{node}")
                current_node.contents.append(node)
                current_node = getAttributeNode
                self.bump_current_location(2)

            # Get call function ----------------------------------------------------------------------------------------
            elif (self.tokens[self.current_location - 1] == IDENTIFIER
                  and self.tokens[self.current_location] == OPERATOR
                  and self.tokens[self.current_location].is_a(callOpenOperator)):
                self.log_debug("Current location identified as call")

                self.bump_current_location(1)
                arguments_ast = self.parse_until(callCloseOperator)
                self.log_dump(f"Got list of arguments as ast: \n{arguments_ast}")

                node = arguments_ast
                self.log_debug(f"New Node is\n{node}")
                current_node.contents.append(node)
                current_node = node

            # Integer --------------------------------------------------------------------------------------------------
            elif self.tokens[self.current_location] == INTEGER:
                self.log_debug("Current location identified as integer")

                self.bump_current_location(1)
                current_node.contents.append(self.tokens[self.current_location])


            else:
                self.log_critical(f"Could not identify what the tokens at {self.current_location} meant")
                self.bump_current_location(1)  # FIXME: This is for testing

        self.pop_logger_name()

    def bump_current_location(self, amount):
        self.log_trace(f"Skipping {amount}")
        self.current_location += amount
