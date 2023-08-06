"""
Colors is responsible for defining color sequences used when printing to the console.
This essentially allows us for assigning the colors to logs without external dependencies



"""


class SequenceName:
    """
    A class for simplifying creating color sequences via only needing the integer value of the sequence

    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '\033[{}m'.format(str(self.value))

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(self) + str(other)


class Foreground255(SequenceName):
    def __str__(self):
        return u"\u001b[38;5;{}m".format(str(self.value))


class Background255(SequenceName):
    def __str__(self):
        return u"\u001b[48;5;{}m".format(str(self.value))


class ForeGroundColors():
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = [SequenceName(i) for i in range(30, 38)]
    BRIGHT_BLACK, BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE = [
        SequenceName(i) for i in range(90, 98)]


class BackGroundColors():
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = [SequenceName(i) for i in range(40, 48)]
    BRIGHT_BLACK, BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE = [
        SequenceName(i) for i in range(100, 108)]


class FontStyles():
    BOLD = SequenceName(1)
    ITALIC = SequenceName(3)
    UNDERSCORE = SequenceName(4)
    STRIKE = SequenceName(9)
    THICK_UNDERSCORE = SequenceName(21)
    RESET = "\33[0;0m"
    REVERSE = SequenceName(7)


def print_255_colors():
    for i in range(0, 256):
        if i < 16 or i > 231:
            print(Foreground255(i) + str(i).ljust(4), end="")
            if i in [15, 255]:
                print(FontStyles.RESET)
            continue

        grouping = i - 15
        print(Foreground255(i) + str(i).ljust(4), end="")
        if grouping % 36 == 0:
            print(FontStyles.RESET)

    for i in range(0, 256):
        if i < 16 or i > 231:
            foreground = 0
            if i == 0:
                foreground = 15
            if i in [j for j in range(232, 244)]:
                foreground = 15
            elif i > 243:
                foreground = 0

            print(Background255(i) + Foreground255(foreground) + str(i).ljust(4), end="")
            if i in [15, 255]:
                print(FontStyles.RESET)
            continue

        grouping = i - 15
        if i == 16:
            print(Background255(i) + Foreground255(15) + str(i).ljust(4), end="")
            continue
        print(Background255(i) + Foreground255(0) + str(i).ljust(4), end="")
        if grouping % 36 == 0:
            print(FontStyles.RESET)


def print_16_colors():
    group_by = 8
    # Standard 8 Colors are 30 - 37
    for i in range(0, group_by):
        print(SequenceName(30 + i) + str(30 + i).ljust(4), end="")
    print()
    # Bright 8 Colors are 90 - 97
    for i in range(0, group_by):
        print(SequenceName(90 + i) + str(90 + i).ljust(4), end="")
    print(FontStyles.RESET)

    # Standard 8 BG Colors are 40 - 47
    for i in range(0, group_by):
        print(SequenceName(40 + i) + str(40 + i).ljust(4), end="")
    print(FontStyles.RESET)
    # Bright 8 Colors are 100 - 107
    for i in range(0, group_by):
        print(SequenceName(100 + i) + str(100 + i).ljust(4), end="")
    print(FontStyles.RESET)


def print_styles():
    for k, v in FontStyles.__dict__.items():
        if not k.startswith("_"):
            print(v + str(k).ljust(4) + FontStyles.RESET)


if __name__ == '__main__':
    print("16 colors")
    print_16_colors()

    print("\n\n255 colors")
    print_255_colors()

    print("\n\nFontStyles")
    print_styles()
