PINK = '\033[35m'
BLUE = '\033[34m'
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'


def colorize(string: str, color: str):
    return color + string + RESET
