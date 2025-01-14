from utilities.common import * 
import pyautogui as pgui 
import pyperclip as clip 

def pgui_write(s):
  clip.copy(s) 
  pgui.hotkey("ctrl", "v")

if False: # test code: 
  pgui.hotkey("win")
  time.sleep(1)
  pgui_write("リモートデスクトップ接続")
  time.sleep(1)
  pgui.hotkey("enter")
