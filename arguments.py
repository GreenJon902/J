import sys

import betterLogger

logger = betterLogger.get_logger("Arguments")

convert_short_to_long_argument = {
    "-i": "--interpret",

    "-c": "--compile",
    "-in": "--in_file",
    "-out": "--out_file"
}


def parse(args: list[str]):
    logger.push_logger_name("parse")
    logger.log_debug("Parsing Arguments")


    path = args.pop(0)

    args2 = list()
    for arg in args:


        args2.append(arg if not any([arg == k or arg == v for k, v in convert_short_to_long_argument.items()]) else
                     (arg if arg in convert_short_to_long_argument.values() else
                      convert_short_to_long_argument[arg]).replace("--", ""))
    args = args2
    logger.log_dump(f"Parsed args into {args} where path={path}")



    instruction: list[str]
    # No Instruction  --------------------------------------------------------------------------------------------------
    if len(args) == 0:
        logger.log_error("No instruction given, run \"J.py -h\" if you need help!")
        sys.exit()


    # Interpret --------------------------------------------------------------------------------------------------------
    elif args[0] == "interpret":
        if len(args) == 2:
            instruction = ["interpret", args[1]]
        elif len(args) == 3:
            if args[1] == "in_file":
                instruction = ["interpret", args[2]]
            else:
                logger.log_error("interpret can only take one positional argument - \"-in  --in_file\", run \"J.py\" "
                                 "-h if you need help!")
                sys.exit()
        else:
            logger.log_error("Too many or too little arguments given for instruction \"interpret\", run \"J.py\" -h if "
                             "you need help!")
            sys.exit()

    # Invalid Instruction ----------------------------------------------------------------------------------------------
    else:
        logger.log_error("Invalid instruction, run \"J.py -h\" if you need help!")
        sys.exit()

    logger.log_debug(f"Instruction is {instruction}")
    logger.pop_logger_name()
