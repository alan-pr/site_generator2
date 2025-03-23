from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


def convert_to_html(text):
    return parse(text)


def parse(text):
    html_text = text
    while True:
        text_type = get_foremost_symbol(html_text)
        if text_type is None:
            break
        html_text = parse_delimiter(html_text, text_type)
    return html_text


def split_text_delimiter(text, delimiter, text_type):
    start = text.find(delimiter)
    end = text.find(delimiter, start + len(delimiter))

    if start == -1 or end == -1:
        return text
    tag = get_tag(text_type)
    before = text[:start]
    middle = text[start + len(delimiter):end]
    after = text[end + len(delimiter):]

    return f"{before}<{tag}>{middle}</{tag}>{after}"


def parse_delimiter(text, text_type):
    delimiter = get_text_type_symbol(text_type)

    if text.count(delimiter) > 1:
        if text.count(delimiter) % 2 == 0:
            html_text = split_text_delimiter(text, delimiter, text_type)
        else:
            html_text = split_text_outer_delimiter(text, delimiter, text_type)
    else:
        html_text = text
    return html_text


def split_text_outer_delimiter(text, delimiter, text_type):
    start = text.find(delimiter)
    end = text.rfind(delimiter)

    if start == -1 or end == -1 or start == end:
        return text
    tag = get_tag(text_type)
    before = text[:start]
    middle = text[start + len(delimiter):end]
    after = text[end + len(delimiter):]

    return f"{before}<{tag}>{middle}</{tag}>{after}"


def get_foremost_symbol(text):
    foremost_text_type = None
    foremost_index = float("inf")

    for text_type in list(TextType):
        if text_type in [TextType.TEXT, TextType.LINK, TextType.IMAGE]:
            continue
        if text.count(get_text_type_symbol(text_type)) < 2:
            continue
        symbol = get_text_type_symbol(text_type)
        current_index = text.find(symbol)
        if 0 <= current_index < foremost_index:
            foremost_index = current_index
            foremost_text_type = text_type

    if foremost_text_type is None:
        return None

    return foremost_text_type


def get_text_type_symbol(text_type):
    match text_type:
        case TextType.BOLD:
            return "**"
        case TextType.ITALIC:
            return "_"
        case TextType.CODE:
            return "`"
        case _:
            raise ValueError(f"Unknown text type: {text_type}")


def get_tag(text_type):
    match text_type:
        case TextType.BOLD:
            return "b"
        case TextType.ITALIC:
            return "i"
        case TextType.CODE:
            return "code"

def is_symbol_valid(symbol):
    match symbol:
        case TextType.BOLD | TextType.ITALIC | TextType.CODE:
            return True
        case _:
            return False


def is_symbol_present(text, symbol):
    return is_symbol_valid(symbol) and text.count(symbol) > 1


text = """**This is a bold text with an _italic text_ inside** and also this
This an italic text_**
This is a `_code text_`
This is another **bold text**
    """
print()
print(convert_to_html(text))