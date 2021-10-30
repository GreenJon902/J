operators = [
    ">",       # Same as python . - __getattr__
    "(", ")",  # Same as python - call function

    "+",       # Same as python - add too integers
]
valid_identifier_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
valid_identifier_type_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
identifier_and_type_separator_character = "_"
invalid_identifier_type_start_characters = "1234567890"

valid_integer_characters = "123456789"
float_required_character = "."
valid_float_characters = valid_integer_characters + float_required_character

newline_characters = [
    ";"
]

ignored_characters = [
    " "
]

IDENTIFIER = "IDENTIFIER"
OPERATOR = "OPERATOR"
INTEGER = "INTEGER"
FLOAT = "FLOAT"
NEWLINE = "NEWLINE"
