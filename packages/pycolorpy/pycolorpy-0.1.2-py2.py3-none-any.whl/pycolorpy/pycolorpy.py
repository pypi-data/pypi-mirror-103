from typing import Union


VALID_OPTIONS = {
    'bright': '\33[1m',
    'dark': '\33[2m',
    'italic': '\33[3m',
    'underline': '\33[4m',
    'blink': '\33[5m',
    'selected': '\33[7m',
    }

VALID_COLORS = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,
    }

def color_options(colored_string: str, options: Union[str, None]) -> str:
    for option in options:
        if option.lower() in VALID_OPTIONS.keys():
            colored_string = VALID_OPTIONS[option.lower()]+colored_string
        else:
            raise Exception(
                'Invalid option used.\n"'+option+
                '" not a valid option.\nValid options are:\n'+
                ', '.join([k for k in VALID_OPTIONS.keys()])
                )
    return colored_string

def color_bg(colored_string: str, background: Union[str, None]) -> str:
    if background in VALID_COLORS.keys():
        return '\33['+str(VALID_COLORS[background]+10)+'m'+colored_string
    raise Exception(
                'Invalid color used.\n"'+background+
                '" not a valid color.\nValid colors are:\n'+
                ', '.join([k for k in VALID_COLORS.keys()])
                )

def colored_string(
    string: str,
    color_number: int,
    options: Union[str, None],
    background: Union[str, None]
    ) -> str:
    colored_string = '\33['+str(color_number)+'m'+string+'\33[0m'
    if options is None and background is None:
        return colored_string
    elif options is not None and background is None:
        return color_options(colored_string, options)
    elif options is None and background is not None:
        return color_bg(colored_string, background)
    elif options is not None and background is not None:
        return color_bg(color_options(colored_string, options), background)

def black(string: str, options: Union[str, None] = None, background: Union[str, None] = None) -> str:
    return colored_string(string, 30, options, background)

def red(string: str, options: Union[str, None] = None, background: Union[str, None] = None) -> str:
    return colored_string(string, 31, options, background)

def green(string: str, options: Union[str, None] = None, background: Union[str, None] = None) -> str:
    return colored_string(string, 32, options, background)

def yellow(string: str, options: Union[str, None] = None, background: Union[str, None] = None) -> str:
    return colored_string(string, 33, options, background)

def blue(string: str, options: Union[str, None] = None, background: Union[str, None] = None) -> str:
    return colored_string(string, 34, options, background)

def magenta(string: str, options: Union[str, None] = None, background: Union[str, None] = None) -> str:
    return colored_string(string, 35, options, background)

def cyan(string: str, options: Union[str, None] = None, background: Union[str, None] = None) -> str:
    return colored_string(string, 36, options, background)

def white(string: str, options: Union[str, None] = None, background: Union[str, None] = None) -> str:
    return colored_string(string, 37, options, background)
