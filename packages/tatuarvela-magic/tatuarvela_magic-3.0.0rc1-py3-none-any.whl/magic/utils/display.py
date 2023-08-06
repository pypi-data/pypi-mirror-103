from sys import stdout


class Emoji:
    # Emoji spacing in terminal is unpredictable
    # These extra spaces appear to fix issues
    FAILURE = "\u274c\ufeff"
    FIRE = "\U0001f525"
    SPARKLE = "\u2728\ufeff"
    SUCCESS = "\u2705\ufeff"
    TIMER = "\u23f1\u0020"
    TRASH = "\U0001f5d1\u0020"
    WIZARD = "\U0001f9d9"


class Colors:
    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    RESET = "\u001b[0m"


def in_color(text, color):
    return f"{color}{text}{Colors.RESET}"


def print_error(error):
    print(f"""{Colors.RED}{Emoji.FIRE} {error}{Colors.RESET}""")


def clear_last_line():
    stdout.write("\033[F")  # back to previous line
    stdout.write("\033[K")  # clear line
