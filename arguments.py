import betterLogger

logger = betterLogger.get_logger("Arguments")

convert_short_to_long_argument = {
    "-i": "--in_file",
    "-o": "--out_file"
}


def parse(args):
    logger.push_logger_name("parse")
    logger.log_debug("Parsing Arguments")

    new_args = {"path": args[0]}

    for key_index in range(1, len(args), 2):
        value_index = key_index + 1

        key, value = (args[key_index] if args[key_index] in convert_short_to_long_argument.values() else
                        convert_short_to_long_argument[args[key_index]]).replace("--", ""), \
                     args[value_index]

        logger.log_dump(f"Get key, value - {key}, {value}")
        new_args[key] = value

    logger.log_dump(f"Parsed args are {new_args}")
    logger.pop_logger_name()
