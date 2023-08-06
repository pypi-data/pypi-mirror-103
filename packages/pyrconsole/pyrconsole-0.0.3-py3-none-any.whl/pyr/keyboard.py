

def go_line(file, row, col, chinese_characters=0):  # @UnusedVariable
    import fileopen
    if (fileopen.is_eclipse_file(file)):
        go_eclipse_line(row, col)
    elif (fileopen.is_ultraedit_file(file)):
        go_ultraedit_line(row, col)


def go_eclipse_line(row, col):
    from pynput.keyboard import Key, Controller
    keyboard = Controller()

    with keyboard.pressed(Key.ctrl):
        keyboard.press('l')
        keyboard.release('l')

    for i in range(len(str(row))):
        keyboard.press(str(row)[i])
        keyboard.release(str(row)[i])

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    for i in range(col):
        keyboard.press(Key.right)  # @UndefinedVariable
        keyboard.release(Key.right)  # @UndefinedVariable


def go_ultraedit_line(row, col):
    from pynput.keyboard import Key, Controller
    keyboard = Controller()

    with keyboard.pressed(Key.ctrl):
        keyboard.press('g')
        keyboard.release('g')

    for i in range(len(str(row))):
        keyboard.press(str(row)[i])
        keyboard.release(str(row)[i])

    keyboard.press('/')
    keyboard.release('/')

    for i in range(len(str(col + 1))):
        keyboard.press(str(col + 1)[i])
        keyboard.release(str(col + 1)[i])

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

