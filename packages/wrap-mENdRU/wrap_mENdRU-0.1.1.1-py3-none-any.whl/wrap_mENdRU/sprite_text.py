"""
Этот модуль содержит команды по управлению текстовыми спрайтами.

Все команды этого модуля должны применяться только к текстовым спрайтам.

Команды этого модуля позволяют получить и поменять настройки вывода текста в текстовых спрайтах.
Например: размер шрифта, цвет текста и другие.
"""
# from wrap_py import text_sprite


def is_text(id: int) -> bool:
    """
    Проверяет, является ли спрайт с указанным номером текстовым спрайтом.
    Возвращает True, если спрайт с указанным номером является текстовым спрайтом.
    False - если не является.

    :param id: Уникальный номер спрайта.
    :return: True, если спрайт с указанным номером является текстовым спрайтом. False - если не является.
    """
    return text_sprite.is_sprite_text(id)


def get_text(id: int) -> str:
    """
    Возвращает текст спрайта.

    :param id: Уникальный номер спрайта.
    :return: Строка. Текст спрайта.
    """
    return text_sprite.get_text(id)


def get_text_color(id: int):
    """
    Возвращает список из трех чисел [R, G, B].
    Три числа обозначают цвет, которым написан текст спрайта.

    :param id: Уникальный номер спрайта.
    :return: список из трех чисел [R, G, B].
    """
    return text_sprite.get_text_color(id)


def get_font_name(id: int) -> str:
    """
    Возвращает строку с названием шрифта, используемого для написания текста.

    Реально может использоваться другой шрифт, если шрифт с этим именем не найден в системе.

    :param id: Уникальный номер спрайта.
    :return: Строка. Название шрифта.
    """
    return text_sprite.get_font_name(id)


def get_font_size(id: int) -> int:
    """
    Возвращает текущий размер шрифта, которым написана надпись.
    Размер шрифта - это приблизительная высота букв шрифта.

    :param id: Уникальный номер спрайта.
    :return: Число. Размер шрифта.
    """
    return text_sprite.get_font_size(id)


def get_font_bold(id: int) -> bool:
    """
    Возвращает True, если у шрифта включена жирность. False - если не включена.

    :param id: Уникальный номер спрайта.
    :return: True, если у шрифта включена жирность. False - если не включена.
    """
    return text_sprite.get_font_bold(id)


def get_font_italic(id: int) -> bool:
    """
    Возвращает True, если у шрифта включен наклон. False - если не включен.

    :param id: Уникальный номер спрайта.
    :return: True, если у шрифта включен наклон. False - если не включен.
    """
    return text_sprite.get_font_italic(id)


def get_font_underline(id: int) -> bool:
    """
    Возвращает True, если у шрифта включено подчеркивание. False - если отключено.

    :param id: Уникальный номер спрайта.
    :return: True, если у шрифта включено подчеркивание. False - если отключено.
    """
    return text_sprite.get_font_underline(id)


def get_back_color(id: int) -> bool:
    """
    Возвращает список из трех чисел [R, G, B].
    Три числа обозначают цвет заднего фона текста.

    Если фон прозрачный, то возвращается None.

    :param id: Уникальный номер спрайта.
    :return: список из трех чисел [R, G, B] или None.
    """
    return text_sprite.get_back_color(id)


def set_text(id: int, text: str):
    """
    Меняет текст спрайта.

    :param id: Уникальный номер спрайта.
    :param text: Строка. Текст спрайта, который нужно установить.
    """
    return text_sprite.set_text(id, text)


def set_text_color(id: int, r: int, g: int, b: int):
    """
    Меняет цвет, которым написан текст спрайта.

    :param id: Уникальный номер спрайта.
    :param r: Красная(red) составляющая цвета.
    :param g: Зеленая(green) составляющая цвета.
    :param b: Синяя(blue) составляющая цвета.
    """
    return text_sprite.set_text_color_rgb(id, r, g, b)


def set_font_name(id: int, font_name: str):
    """
    Меняет шрифт, используемый для написания текста.
    Реально может использоваться другой шрифт, если шрифт с этим именем не будет найден в системе.

    :param id: Уникальный номер спрайта.
    :param font_name: Строка. Название шрифта, который должен использоваться.
    """
    return text_sprite.set_font_name(id, font_name)


def set_font_size(id: int, size: int):
    """
    Меняет размер шрифта.

    :param id: Уникальный номер спрайта.
    :param size: Число. Новый размер шрифта.
    """
    return text_sprite.set_font_size(id, size)


def set_font_bold(id: int, bold: bool):
    """
    Включает или отключает жирность у шрифта.

    :param id: Уникальный номер спрайта.
    :param bold: Жирность. Должен быть равен True, чтобы включить жирность. False - чтобы выключить.
    """
    return text_sprite.set_font_bold(id, bold)


def set_font_italic(id: int, italic: bool):
    """
    Включает или выключает наклон шрифта.

    :param id: Уникальный номер спрайта.
    :param italic: Наклон. Должен быть равен True, чтобы включить наклон. False - чтобы выключить.
    """
    return text_sprite.set_font_italic(id, italic)


def set_font_underline(id: int, underline: bool):
    """
    Включает или выключает подчеркивание шрифта.

    :param id: Уникальный номер спрайта.
    :param underline: Подчеркивание. Должен быть равен True, чтобы включить подчеркивание. False - чтобы выключить.
    """
    return text_sprite.set_font_underline(id, underline)


def set_back_color(id: int, r: int, g: int, b: int):
    """
    Меняет цвет заднего фона текста.

    :param id: Уникальный номер спрайта.
    :param r: Красная(red) составляющая цвета.
    :param g: Зеленая(green) составляющая цвета.
    :param b: Синяя(blue) составляющая цвета.
    """
    return text_sprite.set_back_color_rgb(id, r, g, b)


def set_back_color_transparent(id: int):
    """
    Устанавливает прозрачный задний фон тексту.

    :param id: Уникальный номер спрайта.
    """
    return text_sprite.clean_back_color(id)

def w1():
    global text_sprite
    from wrap_py import text_sprite


w1()
