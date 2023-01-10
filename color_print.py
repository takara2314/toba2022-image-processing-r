def color_print(text, r, g, b):
    color_code = f"\033[38;2;{r};{g};{b}m"
    reset_code = "\033[0m"

    print(color_code + text + reset_code)
