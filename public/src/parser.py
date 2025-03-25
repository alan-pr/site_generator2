from enum import Enum
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


# Constants
TEXT_FORMATS = [TextType.TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE]
TEXT_LINKS = [TextType.LINK, TextType.IMAGE]
LINK_REGEX = r"(?<!\!)\[(.*?)\]\((.*?)\)"
IMAGE_REGEX = r"!\[(.*?)\]\((.*?)\)"


# Static Functions
def convert_to_html(text):
    return parse(text)


def parse(text):
    html_text = text
    while True:
        text_type = get_foremost_symbol(html_text)
        if text_type in TEXT_FORMATS[1:]:
            html_text = parse_delimiter(html_text, text_type)
        elif text_type is TextType.LINK:
            html_text = parse_link_and_image_texts(html_text)
        elif text_type is TextType.TEXT:
            # html_text = parse_plain_text(html_text).replace('\n', ' ')
            html_text = split_multiline_plain_text(html_text)
            break
    return html_text


def parse_delimiter(text, text_type):
    delimiter = get_text_type_symbol(text_type)
    paragraphs = text.split("\n\n")
    html_paragraphs = []

    for paragraph in paragraphs:
        if text.count(delimiter) > 1:
            if text.count(delimiter) % 2 == 0:
                html_text = split_text_delimiter(paragraph, delimiter, text_type)
            else:
                html_text = split_text_outer_delimiter(paragraph, delimiter, text_type)
        else:
            html_text = text
        html_text = add_paragraph_tags(html_text)
        html_paragraphs.append(html_text.replace("\n", ' '))
    return ''.join(html_paragraphs)


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


def split_multiline_plain_text(text):
    html_lines = []
    if text.count("\n\n") > 0:
        paragraphs = text.split("\n\n")
        html_text = ""
        for paragraph in paragraphs:
            html_text = parse_plain_text(paragraph)
            html_lines.append(html_text)
        return ''.join(html_lines)
    return parse_plain_text(text)


def parse_plain_text(text):
    return add_paragraph_tags(text).replace('\n', ' ')


def parse_link_and_image_texts(text):
    html_text = text
    if is_markdown_link_present(text):
        links = extract_markdown_links(text)
        for link in links:
            formatted_link = f"<a href=\"{link[1]}\">{link[0]}</a>"
            html_text = re.sub(LINK_REGEX, formatted_link, html_text, count=1)
    return html_text


def add_paragraph_tags(text):
    if text[:3] == "<p>" and text[-4:] == "</p>":
        return text
    return "<p>" + text + "</p>"


def get_foremost_symbol(text):
    foremost_text_type = None
    foremost_index = float("inf")

    for text_type in list(TextType):
        if text_type in [TextType.TEXT, TextType.LINK, TextType.IMAGE]:
            continue
        if text.count(get_text_type_symbol(text_type)) < 2:
            continue
        if text_type in TEXT_FORMATS[1:]:
            symbol = get_text_type_symbol(text_type)
            current_index = text.find(symbol)
            if 0 <= current_index < foremost_index:
                foremost_index = current_index
                foremost_text_type = text_type
    if foremost_text_type is None:
        return get_non_format_text(text)
    return foremost_text_type


def get_non_format_text(text):
    if is_markdown_link_present(text):
        return TextType.LINK
    return TextType.TEXT



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


def are_formatted_text_symbols_present(text):
    for text_type in TEXT_FORMATS[1:]:
        symbol = get_text_type_symbol(text_type)
        if is_symbol_present(text, symbol):
            return True
    return False


def extract_markdown_images(text):
    return re.findall(IMAGE_REGEX, text)


def extract_markdown_links(text):
    return re.findall(LINK_REGEX, text)


def is_markdown_link_present(text):
    return re.search(LINK_REGEX, text) is not None



text = "Hello\n\n[Google](www.google.com)"
# text = "This is a **bold text**."
print()
print(parse(text))
