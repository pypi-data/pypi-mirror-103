"""
Этот модуль содержит команды для плавного перемещения спрайтов.

Команды этого модуля очень похожи на команды из модуля sprite.
Отличие между ними в том, что команды из этого модуля выполняются медленно. А команды из модуля sprite - мгновенно.

Например, команда move_to_pos модуля sprite перемещает спрайт на новое место мгновенно. А в этом модуле команда будет перемещать его постепенно, так что будет похоже, что спрайт идет.
"""

# from wrap_py import sprite_actions


def move_to(id: int, x: int, y: int, delay: int = 1000):
    """
    Перемещает спрайт на новое место на экране. Спрайт будет перемещаться в течение delay миллисекунд.

    :param id: Уникальный номер спрайта, который нужно переместить.
    :param x: Координата X, на которую нужно переместить спрайт.
    :param y: Координата Y, на которую нужно переместить спрайт.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.move_sprite_to(id, delay, x, y)


def move_left_to(id: int, left: int, delay: int = 1000):
    """
    Перемещает спрайт по координате X таким образом, чтобы расстояние от Левой
    границы окна до Левой границы спрайта было равно left пикселей.

    :param id: Число. Уникальный номер спрайта
    :param left: Число, указывает расстояние от Левой границы окна до Левой границы спрайта.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.set_left_to(id, delay, left)


def move_right_to(id: int, right: int, delay: int = 1000):
    """
    Перемещает спрайт по координате X таким образом, чтобы расстояние от Левой
    границы окна до Правой границы спрайта было равно right пикселей.

    :param id: Число. Уникальный номер спрайта
    :param right: Число, указывает расстояние от Левой границы окна до Правой границы спрайта.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.set_right_to(id, delay, right)


def move_top_to(id: int, top: int, delay: int = 1000):
    """
    Перемещает спрайт по координате Y таким образом, чтобы расстояние от Верхней границы окна
    до Верхней границы спрайта было равно top пикселей.

    :param id: Число. Уникальный номер спрайта
    :param top: Число, указывает расстояние от Верхней границы окна до Верхней границы спрайта.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.set_top_to(id, delay, top)


def move_bottom_to(id: int, bottom: int, delay: int = 1000):
    """
    Перемещает спрайт по координате Y таким образом, чтобы расстояние от Верхней границы окна
    до Нижней границы спрайта было равно bottom пикселей.

    :param id: Число. Уникальный номер спрайта
    :param bottom: Число, указывает расстояние от Верхней границы окна до Нижней границы спрайта.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.set_bottom_to(id, delay, bottom)


def move_centerx_to(id: int, centerx: int, delay: int = 1000):
    """
    Перемещает спрайт по координате X таким образом, чтобы расстояние от Левой границы окна
    до Центра спрайта было равно centerx пикселей.

    :param id: Число. Уникальный номер спрайта
    :param centerx: Число, указывает расстояние от Левой границы окна до Центра спрайта.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.set_centerx_to(id, delay, centerx)


def move_centery_to(id: int, centery: int, delay: int = 1000):
    """
    Перемещает спрайт по координате Y таким образом, чтобы расстояние от Верхней границы окна
    до Центра спрайта было равно centery пикселей.

    :param id: Число. Уникальный номер спрайта
    :param centery:  Число, указывает расстояние от Верхней границы окна до Центра спрайта.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.set_centery_to(id, delay, centery)


def move(id: int, dx: int, dy: int, delay: int = 1000):
    """
    Перемещает спрайт на указанное количество пикселей по координатам X и Y.

    :param id: Число. Уникальный номер спрайта
    :param dx: Число. На сколько пикселей нужно сдвинуть спрайт по оси X.
    :param dy:  Число. На сколько пикселей нужно сдвинуть спрайт по оси Y.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.move_sprite_by(id, delay, dx, dy)


def move_at_angle(id: int, angle: int, distance: int, delay: int = 1000):
    """
    Перемещает спрайт в указанном направлении на указанное расстояние.

    :param id: Уникальный номер спрайта.
    :param angle: Угол, на который будет перемещен спрайт.
    :param distance: Расстояние, на которое будет перемещен спрайт.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.move_sprite_at_angle(id, delay, angle, distance)


def move_at_angle_dir(id: int, distance: int, delay: int = 1000):
    """
    Перемещает спрайт в направлении его взгляда на указанное расстояние.

    :param id: Уникальный номер спрайта.
    :param distance: На сколько пикселей нужно переместить спрайт.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.move_sprite_to_angle(id, delay, distance)


def move_at_angle_point(id: int, x: int, y: int, distance: int, delay: int = 1000):
    """
    Перемещает спрайт в направлении указанной точки на указанное расстояние.

    :param id: Уникальный номер спрайта.
    :param x: Координата X точки, к которой должен перемещаться спрайт.
    :param y: Координата Y точки, к которой должен перемещаться спрайт.
    :param distance: На сколько пикселей нужно переместить спрайт.
    :param delay: за сколько миллисекунд переместить спрайт
    """
    return sprite_actions.move_sprite_to_point(id, delay, x, y, distance)


def set_width(id: int, width: int, delay: int = 1000):
    """
    Изменяет ширину спрайта на указанную.

    :param id: Уникальный номер спрайта.
    :param width: Новая ширина спрайта.
    :param delay: за сколько миллисекунд изменить размер спрайта
    """
    return sprite_actions.change_sprite_width(id, delay, width)


def set_width_proportionally(id: int, width: int, use_modified_prop: bool = False, delay: int = 1000):
    """
    Устанавливает ширину спрайта с сохранением пропорций.

    Меняет размер спрайта так, чтобы его ширина стала равна width.
    Высота спрайта изменится так, чтобы пропорции спрайта не изменились.

    :param id: Уникальный номер спрайта.
    :param width: Новая ширина спрайта. Высота будет расчитана автоматически.
    :param use_modified_prop: Если True, то будут использованы текущие пропорции спрайта. Т.е. пропорции после всех примененных к нему изменений. Если False, то будут использованы оригинальные пропорции спрайта.
    :param delay: за сколько миллисекунд изменить размер спрайта
    """
    return sprite_actions.change_width_proportionally(id, delay, width, use_modified_prop)


def set_width_percent(id: int, width_percent: int, delay: int = 1000):
    """
    Устанавливает ширину спрайта в процентах от его оригинальной ширины.
    Например, если ширина спрайта 20px, то после вызова этой функции с параметром width_percent=200 ширина спрайта станет 40px.

    :param id: Уникальный номер спрайта.
    :param width_percent: Новая ширина спрайта в процентах от оригинальной ширины.
    :param delay: за сколько миллисекунд изменить размер спрайта
    """
    return sprite_actions.change_sprite_width_proc(id, delay, width_percent)


def set_height(id: int, height: int, delay: int = 1000):
    """
    Изменяет высоту спрайта на указанную.

    :param id: Уникальный номер спрайта.
    :param height: Новая высота спрайта.
    :param delay: за сколько миллисекунд изменить размер спрайта
    """
    return sprite_actions.change_sprite_height(id, delay, height)


def set_height_proportionally(id: int, height: int, use_modified_prop: bool = False, delay: int = 1000):
    """
    Устанавливает высоту спрайта с сохранением пропорций.

    Меняет размер спрайта так, чтобы его высота стала равна height.
    Ширина спрайта изменится так, чтобы пропорции спрайта не изменились.

    :param id: Уникальный номер спрайта.
    :param height: Новая высота спрайта. Ширина будет расчитана автоматически.
    :param use_modified_prop: Если True, то будут использованы текущие пропорции спрайта. Т.е. пропорции после всех примененных к нему изменений. Если False, то будут использованы оригинальные пропорции спрайта.
    :param delay: за сколько миллисекунд изменить размер спрайта
    """
    return sprite_actions.change_height_proportionally(id, delay, height, use_modified_prop)


def set_height_percent(id: int, height_percent: int, delay: int = 1000):
    """
    Устанавливает высоту спрайта в процентах от его оригинальной высоты.
    Например, если высота спрайта 20px, то после вызова этой функции с параметром height_percent=200 высота спрайта станет 40px.

    :param id: Уникальный номер спрайта.
    :param height_percent: Новая высота спрайта в процентах от оригинальной высоты.
    :param delay: за сколько миллисекунд изменить размер спрайта
    """
    return sprite_actions.change_sprite_height_proc(id, delay, height_percent)


def set_size(id: int, width: int, height: int, delay: int = 1000):
    """
    Изменяет ширину и высоту спрайта на указанные.

    :param id: Уникальный номер спрайта.
    :param width: Новая ширина спрайта.
    :param height: Новая высота спрайта.
    :param delay: за сколько миллисекунд изменить размер спрайта
    """
    return sprite_actions.change_sprite_size(id, delay, width, height)


def set_size_percent(id: int, width_percent: int, height_percent: int, delay: int = 1000):
    """
    Устанавливает ширину и высоту спрайта в процентах от оригинальных ширины и высоты.
    Например, если размер спрайта 20*50, то после вызова этой функции с параметрами width_percent=200, height_percent=300 размер спрайта станет 40*150.

    :param id: Уникальный номер спрайта.
    :param width_percent: Новая ширина спрайта в процентах от оригинальной ширины.
    :param height_percent: Новая высота спрайта в процентах от оригинальной высоты.
    :param delay: за сколько миллисекунд изменить размер спрайта
    """
    return sprite_actions.change_sprite_size_proc(id, delay, width_percent, height_percent)


def set_angle(id: int, angle_to_look_to: int, delay: int = 1000):
    """
    Поворачивает спрайт так, чтобы он смотрел по указанному углу.

    :param id: Уникальный номер спрайта.
    :param angle_to_look_to: Число. В направлении какого угла должен смотреть спрайт.
    :param delay: за сколько миллисекунд повернуть спрайт
    """
    return sprite_actions.rotate_to_angle(id, delay, angle_to_look_to)


def set_angle_modif(id: int, angle_modif: int, delay: int = 1000):
    """
    Поворачивает спрайт на указанное число градусов от его оригинального угла.

    :param id: Уникальный номер спрайта.
    :param angle_modif: На сколько градусов должен отличаться угол спрайта от его оригинального угла взгляда.
    :param delay: за сколько миллисекунд повернуть спрайт
    """
    return sprite_actions.set_sprite_angle(id, delay, angle_modif)


def set_angle_to_point(id: int, x: int, y: int, delay: int = 1000):
    """
    Меняет угол спрайта так, чтобы он смотрел на указанную точку.

    :param id: Уникальный номер спрайта.
    :param x: Координата X точки, на которую должен смотреть спрайт.
    :param y: Координата Y точки, на которую должен смотреть спрайт.
    :param delay: за сколько миллисекунд повернуть спрайт
    """
    return sprite_actions.rotate_to_point(id, delay, x, y)



def w1():
    global sprite_actions
    from wrap_py import sprite_actions

w1()
