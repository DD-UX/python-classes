import curses
KEY_Q = ord('q') # 113
screen = curses.initscr()  # Creates screen object

curses.noecho()  # Don't show keys
curses.cbreak()  # Receive keys without hitting ENTER
try:
    screen.keypad(True)  # Allow arrows

    x = 30
    y = 30
    while True:
        screen.clear()  # Deletes older content
        screen.addstr(x, y, "x={} y={}".format(x, y))  # Add text
        #screen.addstr(x, y, "x={} y={}".format(x, y))  # Add text
        #screen.addstr(x, y, "x={} y={}".format(x, y))  # Add text
        screen.refresh()  # Shows added content

        key = screen.getch()  # Get input char
        if key == KEY_Q:
            break
        if key == curses.KEY_LEFT:
            y -= 1
        elif key == curses.KEY_RIGHT:
            y += 1
        elif key == curses.KEY_UP:
            x -= 1
        elif key == curses.KEY_DOWN:
            x += 1
finally:
    screen.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()