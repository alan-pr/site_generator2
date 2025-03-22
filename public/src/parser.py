from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class Parser:
    def convert_to_html(self, text):
        return self.__parse(text)


    def __parse(self, text):
        html_text = text
        while True:
            text_type = self.__get_foremost_symbol(html_text)
            if text_type is None:
                break
            html_text = self.__parse_delimiter(html_text, text_type)
        return html_text


    def __parse_delimiter(self, text, text_type):
        html_lines = []
        delimiter = self.__get_text_type_symbol(text_type)
        lines = text.split('\n')

        for line in lines:
            if line.count(delimiter) > 1:
                if line.count(delimiter) % 2 == 0:
                    html_text = self.__split_text_delimiter(line, delimiter, text_type)
                else:
                    html_text = self.__split_text_outer_delimiter(line, delimiter, text_type)
            else:
                html_text = line
            html_lines.append(html_text)

        return '\n'.join(html_lines)


    def __get_text_type_symbol(self, text_type):
        match text_type:
            case TextType.BOLD:
                return "**"
            case TextType.ITALIC:
                return "_"
            case TextType.CODE:
                return "`"
            case _:
                raise ValueError(f"Unknown text type: {text_type}")


    def __split_text_outer_delimiter(self, text, delimiter, text_type):
        head_delimiter_index = text.find(delimiter)
        tail_delimiter_index = text.rfind(delimiter)
        delimiter_text = text[head_delimiter_index:tail_delimiter_index].replace(delimiter, f"<{self.__get_tag(text_type)}>", 1)
        head_text = text[:head_delimiter_index]
        tail_text = text[tail_delimiter_index:].replace(delimiter, f"</{self.__get_tag(text_type)}>")
        return  head_text + delimiter_text + tail_text


    def __split_text_delimiter(self, text, delimiter, text_type):
        head_text = text[:text.find(delimiter)]
        delimiter_text = text[text.find(delimiter):].lstrip(delimiter)
        tail_text = delimiter_text[delimiter_text.find(delimiter):].lstrip(delimiter)
        delimiter_text = delimiter_text[:delimiter_text.find(delimiter)]
        return head_text + f"<{self.__get_tag(text_type)}>" + delimiter_text + f"</{self.__get_tag(text_type)}>" + tail_text


    def __get_tag(self, text_type):
        match text_type:
            case TextType.BOLD:
                return "b"
            case TextType.ITALIC:
                return "i"
            case TextType.CODE:
                return "code"


    def __get_foremost_symbol(self, text):
        foremost_text_type = None
        foremost_index = float("inf")

        for text_type in list(TextType):
            if text_type in [TextType.TEXT, TextType.LINK, TextType.IMAGE]:
                continue
            if text.count(self.__get_text_type_symbol(text_type)) < 2:
                continue
            symbol = self.__get_text_type_symbol(text_type)
            current_index = text.find(symbol)
            if 0 <= current_index < foremost_index:
                foremost_index = current_index
                foremost_text_type = text_type

        if foremost_text_type is None:
            return None

        return foremost_text_type




    def __is_symbol_present(self, text, symbol):
        if self.__is_symbol_valid(symbol):
            return text.count(symbol) > 1


    def __is_symbol_valid(self, symbol):
        match symbol:
            case TextType.BOLD | TextType.ITALIC | TextType.CODE:
                return True
            case _:
                return False


text = """**This is a bold text with an _**italic text_** inside** and** also this**
This an italic text_
This is a `_code text_`
This is another **bold text**
    """
parser = Parser()
print(parser.convert_to_html(text))