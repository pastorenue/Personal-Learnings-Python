import keyboard

def keyboard_press(event):
   print(f"{event.name} was pressed")


if __name__ == "__main__":
    keyboard.on_press(keyboard_press)
    keyboard.wait('esc')