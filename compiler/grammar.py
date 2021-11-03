# Operators ------------------------------------------------------------------------------------------------------------
getAttributeOperator = ">"
callOpenOperator = "("
callCloseOperator = ")"
evaluateSectionBeforeOpenOperator = "("
evaluateSectionBeforeCloseOperator = ")"

additionOperator = "+"

argumentSeparatorOperator = ","

arithmeticOperators = [
    additionOperator
]

operators = [
    getAttributeOperator,  # Same as python . - __getattr__
    callOpenOperator, callCloseOperator,  # Same as python - call function
    evaluateSectionBeforeOpenOperator, evaluateSectionBeforeCloseOperator,  # Same as python - change the order of
                                                                            #                  evaluation

    "+",  # Same as python - add too integers

    argumentSeparatorOperator  # Same as python - separate arguments
]
# Identifier -----------------------------------------------------------------------------------------------------------
valid_identifier_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
valid_identifier_type_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
invalid_identifier_type_start_characters = "1234567890"

identifier_and_type_separator_character = "_"
# Numeric --------------------------------------------------------------------------------------------------------------
valid_integer_characters = "123456789"

float_required_character = "."
valid_float_characters = valid_integer_characters + float_required_character
# Other ----------------------------------------------------------------------------------------------------------------
newline_characters = [
    ";"
]

ignored_characters = [
    " ",
    "\n"
]
# ----------------------------------------------------------------------------------------------------------------------
