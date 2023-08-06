def debug_print(message: str) -> None:
    """Print a message accompanied by info about the file, line number, and caller."""
    import inspect
    import os

    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print(
        os.getpid(),
        info.filename,
        "func=%s" % info.function,
        "line=%s:" % info.lineno,
        message,
    )
