import pyautogui
import time
pyautogui.PAUSE = 2
pyautogui.FAILSAFE = True
currentscrn_name = "screenshot.png"
currentscrn = pyautogui.screenshot(currentscrn_name)