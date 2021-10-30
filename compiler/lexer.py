import pprint

from betterLogger import ClassWithLogger, push_name_to_logger_name_stack

from compiler import token_types
from compiler.token_types import IDENTIFIER, OPERATOR, valid_identifier_type_characters, \
    identifier_and_type_separator_character, valid_identifier_characters, INTEGER, FLOAT, float_required_character, \
    ignored_characters, valid_float_characters, newline_characters, NEWLINE


class Lexer(ClassWithLogger):
    J_code: str
    file_path: str
    current_location: int = 0
    amount_to_skip: int = 0

    def __init__(self, J_code, file_path):
        ClassWithLogger.__init__(self)

        self.J_code = J_code
        self.file_path = file_path

        self.push_logger_name(f"\"{self.file_path}\"")

    @push_name_to_logger_name_stack
    def get_tokens(self):
        self.log_debug("Getting tokens for self")
        self.log_trace(f"Script is:\n{self.J_code}")

        tokens = list()

        self.current_location = 0
        while self.current_location < len(self.J_code):
            self.log_dump(f"Current location is {self.current_location} which is "
                          f"\"{self.J_code[self.current_location]}\"")

            if self.is_current_location_ignored():
                self.log_dump("Current location was skipped")
                self.current_location += 1

            else:
                tokens.append(self.get_token_at_current_location())


                self.log_trace(f"Skipping {self.amount_to_skip}")

                if self.amount_to_skip == 0:
                    self.amount_to_skip = 1
                    self.log_error(f"Amount to skip was 0 when current location {self.current_location}")

                self.current_location += self.amount_to_skip
                self.amount_to_skip = 0

        self.log_debug(f"Got tokens:\n{pprint.pformat(tokens)}")

        return tokens


    def get_token_at_current_location(self):
        self.push_logger_name(f"get_token_at_current_location({self.current_location})")


        token_types_to_check = (
            (NEWLINE, self.get_if_current_location_is_newline),
            (OPERATOR, self.get_if_current_location_is_operator),
            (FLOAT, self.get_if_current_location_is_float),
            (INTEGER, self.get_if_current_location_is_integer),
            (IDENTIFIER, self.get_if_current_location_is_identifier)
        )


        ret = None


        for token_type_to_check, function in token_types_to_check:
            token_value = function()
            if ret is None and token_value is not None:
                ret = token_type_to_check, token_value
                self.log_debug(f"Token at {self.current_location} was an {token_type_to_check}, the value of the token "
                               f"was \"{token_value}\"")

                break

        if ret is None:
            ret = None, None
            self.log_error(f"Could not figure out which token was at {self.current_location}")

        self.log_trace(f"Returning {ret}")
        self.pop_logger_name()
        return ret


    def is_current_location_ignored(self):
        self.push_logger_name(f"is_current_location_ignored({self.current_location})")

        ret = self.J_code[self.current_location] in ignored_characters

        self.log_trace(f"Returning {ret}")
        self.pop_logger_name()
        return ret

    def get_if_current_location_is_newline(self):
        self.push_logger_name(f"get_if_current_location_is_newline({self.current_location})")

        ret = None
        for character in newline_characters:
            fail = False

            char_index = 0
            for char_index, char in enumerate(newline_characters):
                if not self.J_code[self.current_location + char_index] == char:
                    fail = True
                    break

            if not fail:
                self.amount_to_skip += (char_index + 1)
                ret = character

        self.log_trace(f"Returning {ret}")
        self.pop_logger_name()
        return ret

    def get_if_current_location_is_operator(self):
        self.push_logger_name(f"get_if_current_location_is_operator({self.current_location})")

        ret = None
        for operator in token_types.operators:
            fail = False

            char_index = 0
            for char_index, char in enumerate(operator):
                if not self.J_code[self.current_location + char_index] == char:
                    fail = True
                    break

            if not fail:
                self.amount_to_skip += (char_index + 1)
                ret = operator

        self.log_trace(f"Returning {ret}")
        self.pop_logger_name()
        return ret


    def get_if_current_location_is_identifier(self):
        self.push_logger_name(f"get_if_current_location_is_identifier({self.current_location})")

        identifier_string = ""
        n = 0

        current_part_number = 0
        while True:
            current_character = self.J_code[self.current_location + n]
            if (current_part_number == 0 or current_part_number == 2) and current_character in \
                    valid_identifier_type_characters:
                identifier_string += current_character

            elif current_part_number == 1 and current_character in valid_identifier_characters:
                identifier_string += current_character

            elif current_character == identifier_and_type_separator_character:
                identifier_string += current_character
                current_part_number += 1

            else:
                amount = identifier_string.count(identifier_and_type_separator_character)
                if amount == 1 or amount == 2:
                    break

                self.log_error(f"Invalid identifier at {self.current_location + n}")
                identifier_string = ""
                break

            n += 1

        ret = None if len(identifier_string) == 0 else identifier_string
        self.amount_to_skip += n

        self.log_trace(f"Returning {ret}")
        self.pop_logger_name()
        return ret


    def get_if_current_location_is_float(self):
        self.push_logger_name(f"get_if_current_location_is_float({self.current_location})")

        float_string = ""
        n = 0
        while True:
            current_character = self.J_code[self.current_location + n]

            if current_character in valid_float_characters:
                float_string += current_character

            else:
                if float_required_character not in float_string:
                    float_string = ""
                    n = 0
                break

            n += 1

        ret = None if len(float_string) == 0 else float_string
        self.amount_to_skip += n

        self.log_trace(f"Returning {ret}")
        self.pop_logger_name()
        return ret


    def get_if_current_location_is_integer(self):
        self.push_logger_name(f"get_if_current_location_is_integer({self.current_location})")

        int_string = ""
        n = 0
        while True:
            current_character = self.J_code[self.current_location + n]

            if current_character in valid_float_characters:
                int_string += current_character

            else:
                break

            n += 1

        ret = None if len(int_string) == 0 else int_string
        self.amount_to_skip += n

        self.log_trace(f"Returning {ret}")
        self.pop_logger_name()
        return ret
