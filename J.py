import pprint

if __name__ == '__main__':
    import os
    import info

    os.environ["APPNAME"] = info.name
    os.environ["SHORT_APPNAME"] = info.name
    os.environ["APPAUTHOR"] = info.author
    os.environ["APPVERSION"] = info.version

    log_names_to_shorten = {
        "get_token_at_current_location": "gtacl",
        "get_if_current_location_is_newline": "gicli_newline",
        "get_if_current_location_is_operator": "gicli_operator",
        "get_if_current_location_is_float": "gicli_float",
        "get_if_current_location_is_integer": "gicli_integer",
        "get_if_current_location_is_identifier": "gicli_identifier",
        "is_current_location_ignored": "icli"
    }
    os.environ["LOG_NAMES_TO_SHORTEN"] = repr(dict(eval(os.environ["LOG_NAMES_TO_SHORTEN"])).update(
        log_names_to_shorten)) if os.environ.get("LOG_NAMES_TO_SHORTEN") is not None else repr(log_names_to_shorten)


    import betterLogger
    setup_logger = betterLogger.get_logger("Setup")

    import sys
    args = sys.argv
    setup_logger.log_trace(f"Ran with args - {args}")

    import arguments
    instruction_and_args = arguments.parse(args)
    instruction, args = instruction_and_args[0], instruction_and_args[1:]
    setup_logger.log_dump(f"Split into instruction={instruction}, args={args}")

    J_logger = betterLogger.get_logger("J")

    if instruction == "interpret":
        J_code = open(args[0], "r").read()
        J_logger.log_info("Loaded J file")
        J_logger.log_debug(f"Contents are:\n{J_code}")

        from compiler.lexer import Lexer
        tokens = Lexer(J_code, args[0]).get_tokens()
        J_logger.log_info("Tokenized J file")
        J_logger.log_debug(f"Tokens are:\n{pprint.pformat(tokens)}")

        from compiler.parser import Parser
        ast = Parser(tokens, args[0]).get_ast()
        J_logger.log_info("Parsed tokens from J file")

        J_logger.log_debug(f"Parsed tokens are:\n{pprint.pformat(ast)}")
