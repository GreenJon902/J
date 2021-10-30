if __name__ == '__main__':
    import os
    import info

    os.environ["APPNAME"] = info.name
    os.environ["SHORT_APPNAME"] = info.name
    os.environ["APPAUTHOR"] = info.author
    os.environ["APPVERSION"] = info.version

    import betterLogger
    setup_logger = betterLogger.get_logger("Setup")

    import sys
    args = sys.argv
    setup_logger.log_trace(f"Ran with args - {args}")

    import arguments
    instruction_and_args = arguments.parse(args)
    instruction, args = instruction_and_args[0], instruction_and_args[1:]
    setup_logger.log_dump(f"Split into instruction={instruction}, args={args}")

    if instruction == "interpret":
        J_code = open(args[0], "r").read()

        from compiler.lexer import Lexer
        tokens = Lexer(J_code, args[0]).get_tokens()
