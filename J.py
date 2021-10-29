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
    print(sys.argv, os.environ)
    setup_logger.log_trace(f"Ran with args - {args}")

