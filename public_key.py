import pyautogui as kb
import time
import random as rng

# Enable failsafe: move mouse to top-left corner to stop
kb.FAILSAFE = True

try:
    while True:
        delay = rng.uniform(3, 5)  # random delay between scrolls
        kb.scroll(-500)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(-300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(-300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(-300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(-300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(-300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(-500)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(-300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(-300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(500)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(300)            # negative = scroll down
        time.sleep(delay)
        kb.scroll(300)            # negative = scroll down
        time.sleep(delay)
except KeyboardInterrupt:
    print("Script stopped manually.")
