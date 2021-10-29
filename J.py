if __name__ == '__main__':
    import os
    import info

    os.environ["APPNAME"] = info.name
    os.environ["SHORT_APPNAME"] = info.name
    os.environ["APPAUTHOR"] = info.author
    os.environ["APPVERSION"] = info.version

    import betterLogger
    setup_logger = betterLogger.get_logger("Setup")

    setup_logger.log_info("Hello World!")


