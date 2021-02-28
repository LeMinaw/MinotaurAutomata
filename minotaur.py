#!/usr/bin/env python3

"""Simple, quick-and-dirty CLI application showcasing Minotaur generation.
#NoQA on this :)
"""

import curses

from labyrinths import MinotaurLabyrinth, minotaur_rule_randomized


def main(screen):
    curses.curs_set(False)
    curses.halfdelay(1) # 0.1s 
    w, h = curses.COLS, curses.LINES

    automata = MinotaurLabyrinth((w-1, h-1))
    # Uncomment the following line to tweak the cellular automata deterministic
    # generation by adding a bit of random to it
    # automata.rule = minotaur_rule_randomized
    automata.seed(4)

    while True:
        screen.clear()
        screen.addstr(0, 0, str(automata))
        screen.addstr(
            h-1, 0,
            "MINOTAUR::AUTOMATA",
            curses.A_REVERSE
        )
        screen.addstr(
            h-1, w-67,
            "RETURN: re-seed // RIGHT: frameskip // SPACE: pause // Other: quit",
            curses.A_REVERSE
        )
        screen.refresh()

        key = screen.getch()
        # No input after timer finishes or left/down key pressed
        if key not in (curses.ERR, 0x102, 0x105, 0x1C6, 0x1C8):
            # Return key pressed
            if key == 0xA:
                automata.empty()
                automata.seed(4)
                continue
            # Spacebar pressed
            elif key == 0x20:
                screen.addstr(
                    0, 0,
                    "::PAUSED::",
                    curses.A_REVERSE
                )
                screen.refresh()
                while screen.getch() == curses.ERR:
                    pass
                continue
            break
        
        automata.tick_world()


if __name__ == '__main__':
    curses.wrapper(main)
