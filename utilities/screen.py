import curses


def screen_helper(callback):
    # Creates screen object
    screen = curses.initscr()
    curses.curs_set(False)
    is_active = True
    screen.keypad(True)

    def close_callback():
        nonlocal is_active
        is_active = False
        return

    try:
        while is_active:
            # Allow arrows
            screen.clear()

            # Send screen access
            callback(screen, close_callback)

            # Shows added content
            screen.refresh()
    except IndexError:
        print("Screen size limit reached")
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        screen.keypad(False)

    return

